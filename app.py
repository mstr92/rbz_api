import os
import logging.config

from flask import Flask, Blueprint
from helpers.restplus import api
from settings import *
from endpoints.movies import ns as namespace_movie
from database import db


def configure_app(flask_app):
    #flask_app.config['SERVER_NAME'] = FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = RESTPLUS_ERROR_404_HELP


def create_app():
    flask_app = Flask(__name__)
    configure_app(flask_app)
    with flask_app.app_context():
        db.init_app(flask_app)
    return flask_app


app = create_app()

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
log = logging.getLogger(__name__)


def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(namespace_movie)
    api.add_namespace(namespace_general)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    #app.run(host='129.27.153.16', port=5000, ssl_context='adhoc')
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()