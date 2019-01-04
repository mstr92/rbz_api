import logging
import json
import requests

from helpers.restplus import api
from flask_restplus import Resource
from helpers.serializers import movie, user, backup
from flask import request, abort, jsonify
from settings import APPKEY, SECONDS_TO_WAIT_FOR_RESPONSE, API_KEY_TMDB
from tasks.tasks import *
from database.db_functions import *
from flask import Response
from functools import wraps

log = logging.getLogger(__name__)
ns = api.namespace('rbz/general', description='General Functions')


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
        Insert new Device with given UUID
        """
        modelObject = set_uuid(uuid)
        if modelObject:
            return 201
        else:
            return 401



@ns.route('/user')
class DatabaseUser(Resource):

    @api.expect(user)
    @api.response(201, 'User registered in database')
    @api.response(401, 'Error: User not registered!')
    def post(self):
        """
        Insert new User
        """
        data = request.json

        modelObject = set_user(data['username'], data['email'], data['password'])
        if modelObject:
            return 201
        else:
            return 401


@ns.route('/backup')
@ns.route('/backup/<int:user_id>')
class DatabaseUser(Resource):

    @api.expect(backup)
    @api.response(201, 'User registered in database')
    @api.response(401, 'Error: User not registered!')
    def post(self):
        """
        Insert Backup Objects for user
        """
        data = request.json

        modelObject = set_backup(data['user_id'], data['history'], data['rating'], data['favourite'])
        if modelObject:
            return 201
        else:
            return 401

    @api.response(201, 'Entry exists')
    def get(self, user_id):
        modelObject = get_backup(user_id)
        print(json.dumps(modelObject))
        return 201