import os
import time

from celery import Celery
from celery.task import Task
from engine.connections import send_request_to_movie_engine

# from db import get_db_connection

## Broker settings.
BROKER_URL = u'amqp://guest:guest@{addr}:{port}//'.format(
    addr="rabbit1",
    port=5672,
)


celery_app = Celery('tasks', backend='amqp', broker=BROKER_URL)

class CalculateAndSaveResponse(Task):

    queue = 'movies'

    def __init__(self, *args, **kwargs):
        self.connection = None  #kwargs.get('connection', get_db_connection())

    # Wrap the celery app within the Flask context
    def bind(self, app):
        return super(self.__class__, self).bind(celery_app)

    def run(self, id, request):
        retval = send_request_to_movie_engine("**m:the dark knight**")
        return retval

    def on_success(self, retval, task_id, args, kwargs):
        # from app import create_app
        print('SUCCESS')
        print(os.environ['RABBITMQ_PORT_5672_TCP_ADDR'])
        print(os.environ['RABBITMQ_PORT_5672_TCP_PORT'])

        # Save calculated response in database
        # app = create_app()
        # app.app_context().push()

        # db.session.query(DataModel).filter(DataModel.id == args[0]).update({'response': retval})
        # db.session.commit()
        # return "Success"

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("ERROR: No Response calculated!")


