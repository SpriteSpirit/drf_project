from rest_framework import serializers

from vehicle.models import Car, Moto, Milage
from vehicle.services import convert_currencies
from vehicle.validators import TitleValidator


class MilageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milage
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    last_milage = serializers.IntegerField(source='milage.all.first.milage', read_only=True)
    milage = MilageSerializer(many=True, read_only=True)
    usd_price = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = '__all__'

    def get_usd_price(self, instance):
        return convert_currencies(instance.price)


class MotoSerializer(serializers.ModelSerializer):
    last_milage = serializers.IntegerField(source='milage.all.first.milage', required=False, allow_null=True)

    class Meta:
        model = Moto
        fields = '__all__'

    def get_last_milage(self, instance):
        if instance.milage.all().first():
            return instance.milage.all().first().milage
        return 0


class MotoMilageSerializer(serializers.ModelSerializer):
    moto = MotoSerializer()

    class Meta:
        model = Milage
        fields = ('milage', 'year', 'moto',)


class MotoCreateSerializer(serializers.ModelSerializer):
    milage = MilageSerializer(many=True)

    class Meta:
        model = Moto
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Moto.objects.all()),
        ]

    def create(self, validated_data):
        milage = validated_data.pop('milage')

        moto_item = Moto.objects.create(**validated_data)

        # создается новый пробег с указание на то, что это ссылка на машину
        for m in milage:
            Milage.objects.create(moto=moto_item, **m)

        return moto_item
