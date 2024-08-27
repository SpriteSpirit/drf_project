from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from vehicle.models import Car, Moto, Milage
from vehicle.paginators import VehiclePaginator
from vehicle.permissions import IsOwnerOrStaff
from vehicle.serializers import CarSerializer, MotoSerializer, MilageSerializer, MotoMilageSerializer, \
    MotoCreateSerializer
from vehicle.tasks import check_milage


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [AllowAny]  # [IsAuthenticated]


class MotoCreateAPIView(generics.CreateAPIView):
    serializer_class = MotoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()
        # new_moto = serializer.save()
        # new_moto.owner = self.request.user
        # new_moto.save()


class MotoListAPIView(generics.ListAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    pagination_class = VehiclePaginator


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MotoSerializer
    queryset = Moto.objects.all()
    permission_classes = [IsOwnerOrStaff]


class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Moto.objects.all()


class MotoMillageListAPIView(generics.ListAPIView):
    serializer_class = MotoMilageSerializer
    queryset = Milage.objects.filter(moto__isnull=False)


class MilageCreateAPIView(generics.CreateAPIView):
    serializer_class = MilageSerializer

    def perform_create(self, serializer):
        new_milage = serializer.save()

        if new_milage.car:
            check_milage.delay(new_milage.car.id, "Car")
        else:
            check_milage.delay(new_milage.moto.id, "Moto")


class MilageListAPIView(generics.ListAPIView):
    serializer_class = MilageSerializer
    queryset = Milage.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('moto', 'car')
    ordering_fields = ('year',)
