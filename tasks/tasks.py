import os
import time

from celery import Celery
from celery.task import Task
from engine.connections import send_request_to_movie_engine
from settings import RABBIT_PORT, RABBIT_HOST
from database.db_functions import set_response

# from db import get_db_connection

## Broker settings.
BROKER_URL = u'amqp://guest:guest@{addr}:{port}//'.format(
    addr=RABBIT_HOST,
    port=RABBIT_PORT,
)

celery_app = Celery('tasks', backend='amqp', broker=BROKER_URL)

class CalculateAndSaveResponse(Task):
    queue = 'movies'

    def run(self, id, request):
        retval = send_request_to_movie_engine("**m:the dark knight**")
        return retval

    def on_success(self, retval, task_id, args, kwargs):
        print('SUCCESS')
        set_response(args[0], retval)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("ERROR: No Response calculated!")


