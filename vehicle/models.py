from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Car(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return self.title


class Moto(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Мотоцикл"
        verbose_name_plural = "Мотоциклы"

    def __str__(self):
        return self.title


class Milage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, **NULLABLE)
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, **NULLABLE)

    milage = models.PositiveIntegerField(verbose_name="Пробег")
    year = models.PositiveSmallIntegerField(verbose_name="Год регистрации")

    class Meta:
        verbose_name = "Пробег"
        verbose_name_plural = "Пробег"
        ordering = ("-year",)

    def __str__(self):
        return f"{self.moto if self.moto else self.car} {self.year} года"
    