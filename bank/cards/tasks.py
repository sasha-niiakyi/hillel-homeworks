from time import sleep
from datetime import datetime

from celery import shared_task

from .models import Card, Status

@shared_task
def activate(pk: int):
	sleep(120)
	card = Card.objects.get(pk=pk)
	card.status = Status.objects.get(pk=2)
	card.save()


@shared_task
def freezing():
	cards = Card.objects.filter(expir_date__gt=str(datetime.now().date()), 
								status__in=Status.objects.exclude(pk=4))
	for card in cards:
		card.status = Status.objects.get(pk=4)
		card.save()
