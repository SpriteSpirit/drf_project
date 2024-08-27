import json
from datetime import datetime, timedelta

import requests
from celery.schedules import schedule
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework import status

from config import settings


def convert_currencies(rub_price):
    usd_price = 0
    response = requests.get(
        f'{settings.CURRENCY_API_URL}v3/latest?apikey={settings.CURRENCY_API_KEY}&currencies=RUB')

    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()['data']['RUB']['value']
        usd_price = int(float(rub_price) * usd_rate)
        print(response.json())

    return usd_price


def set_schedule(*args, **kwargs):
    """ Задать расписание """

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
        name='Update every 10 seconds',  # a descriptive name for the schedule.
    )
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='Importing contacts',  # simply describes this periodic task.
        task='proj.tasks.import_contacts',  # name of task.
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
