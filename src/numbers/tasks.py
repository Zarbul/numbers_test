from datetime import datetime

from celery import shared_task
from celery.schedules import crontab
# from loguru import logger

from config.celery import app
from src.numbers import models
from src.numbers import services

app.conf.beat_schedule = {
    """
    Example:
    'add-5-minute-update': {
        'task': 'process.tasks.update_youtube_channel_stat',
        'schedule': crontab(minute='*/5')  # executes every 5 minutes
        or
        'schedule': crontab(minute='*/30')   # executes every 30 minutes
        or
        'schedule': crontab(hour='*/1')   # executes every hour
    },
    """

    'create_or_update_db_record': {
        'task': 'src.numbers.tasks.create_or_update_db_record',
        'schedule': crontab(minute='*/10')
    },
}


@app.task()
def create_or_update_db_record():
    rate = services.get_rate()
    values = services.get_data_from_sheet()
    for row in values:
        models.Order.objects.update_or_create(
            order_number=int(row[1]),
            defaults=dict(
                price_in_usd=int(row[2]),
                date_to_delivery=datetime.strptime(row[3], '%d.%m.%Y').date(),
                price_in_rub=int(row[2]) * float(rate)
            )
        )
