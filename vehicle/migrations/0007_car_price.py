# Generated by Django 5.1 on 2024-08-27 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicle", "0006_car_owner_moto_owner"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=12, verbose_name="Цена"
            ),
        ),
    ]
