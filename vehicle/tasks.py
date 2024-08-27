import logging

from celery import shared_task
# from django.core.mail import send_mail
from vehicle.models import Car, Moto

logging.basicConfig(level=logging.INFO)


@shared_task
def check_milage(pk, model):
    """ Проверка, что пробег возрастает """
    if model == 'Car':
        instance = Car.objects.filter(pk=pk).first()
    else:
        instance = Moto.objects.filter(pk=pk).first()

    if instance:
        prev_milage = -1

        for m in instance.milage.all():
            if prev_milage == -1:
                prev_milage = m.milage
            else:
                if prev_milage < m.milage:
                    print('Неверный пробег')
                    break


@shared_task
def check_filter():
    """ Проверка фильтров """

    filter_price = {'price__lte': 50000}

    if Car.objects.filter(**filter_price).exists():
        logging.info('Отчет по фильтру\nМашины с ценой не более 50000')
    print('Отчет по фильтру\nМашины с ценой не более 50000')
        # send_mail(
        #     subject='Отчет по фильтрам',
        #     message='У нас есть машины по вашей выборке',
        #     from_email='admin@example.com',
        #     recipient_list=['user@example.com'],
        #     )

