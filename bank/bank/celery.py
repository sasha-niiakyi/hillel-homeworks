import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
django.setup()

from celery import Celery
from celery.schedules import crontab
from cards.tasks import freezing


app = Celery('bank')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(crontab(minute=0, hour=0), freezing.s(), name='freeze every day')

@app.task(bind=True, ignore_result=True)
def debug_task(self):
	print(f'Request: {self.request!r}')

# @app.task
# def test():
# 	print(2 + 2)