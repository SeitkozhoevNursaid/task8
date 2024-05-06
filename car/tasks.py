from celery import shared_task
from car.telegram import polling_thread


@shared_task
def run_telegram_bot():
    polling_thread()
