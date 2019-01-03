import logging
import json

from helpers.restplus import api
from flask_restplus import Resource
from helpers.serializers import movie
from flask import request, abort
from settings import APPKEY, SECONDS_TO_WAIT_FOR_RESPONSE
from tasks.tasks import *
from database.db_functions import *
from flask import Response
from functools import wraps

log = logging.getLogger(__name__)
ns = api.namespace('rbz/movies', description='Reddit Movie Thread')


# Decorator function to check if API-Key is valid
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == APPKEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@ns.route('/')
class BotRequest(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.expect(movie)
    @require_appkey
    def post(self):
        """
        Make a request to Movie Recommendation Server
        """
        data = request.json

        # Check if parent exists in database
        parentId, parentResponse = check_if_entry_exists(json.dumps(data))

        # Create new database entry and get entry id
        # If parent exists, the parentId and the parentResponse get set
        if parentResponse is None:
            parentId = None

        id = create_entry(json.dumps(data), parentResponse, parentId)
        # Check if response has to be calculated else return response
        if parentResponse is None:

            CalculateAndSaveResponse.delay(id, json.dumps(data))

            # Check if response is calculated after 5 seconds
            # If true, return calculated response
            # else return id
            time.sleep(SECONDS_TO_WAIT_FOR_RESPONSE)
            modelObject = get_entry(id)

            if modelObject.response == None:
                return Response(response=str(id), mimetype='text/plain')
            else:
                return Response(response=str(modelObject.response), mimetype='text/plain')
        else:
            return Response(parentResponse, mimetype='text/plain')



@ns.route('/<int:id>')
class BotResponse(Resource):

    @api.header('key', 'API-Key', required=True)
    @api.response(201, 'Object found, calculation finished')
    @api.response(404, 'Object not found.')
    @api.response(405, 'Calculation of response not finished.')
    @require_appkey
    def get(self, id):
        """
        Return a response with given ID.
        """
        # Get Object from database with id
        modelObject = get_entry(id)

        # Check if object in database
        if modelObject == None:
            return None, 404

        # Check if object response is set
        if modelObject.response == None:
            return None, 405
        else:
            return modelObject.response, 201


@ns.route('/genre/<string:text>')
class BotTest(Resource):

    @api.response(201, 'Object found, calculation finished')
    @api.response(404, 'Object not found.')
    def get(self, text):
        """
        Return a response with given ID.
        """

        # Get Object from database with id
        modelObject = get_genre(text)

        print(json.dumps([(dict(row.items())) for row in result]))
        # Check if object response is set
        # if modelObject == None:
        #     return  None, 404
        # else:
        return "", 201

