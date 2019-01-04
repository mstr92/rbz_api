import logging
import json
import requests

from helpers.restplus import api
from flask_restplus import Resource
from helpers.serializers import movie
from flask import request, abort, jsonify
from settings import APPKEY, SECONDS_TO_WAIT_FOR_RESPONSE, API_KEY_TMDB
from tasks.tasks import *
from database.db_functions import *
from flask import Response
from functools import wraps

log = logging.getLogger(__name__)
ns = api.namespace('rbz/general', description='Reddit Movie Thread')


# Decorator function to check if API-Key is valid
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == APPKEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@ns.route('/uuid/<string:uuid>')
class DatabaseUUID(Resource):

    @api.response(201, 'Object found')
    def post(self, uuid):
        """
        Return a response with given ID.
        """
        modelObject = set_uuid(uuid)
        print(modelObject)
        return "", 201