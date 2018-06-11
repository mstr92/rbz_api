# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/rbz_api'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db/rbz_api'
SQLALCHEMY_TRACK_MODIFICATIONS = False

APPKEY = 'ABCD1234'

# Engine
ENGINE_HOST = '129.27.153.16'
ENGINE_PORT = 8008

#RabbitMQ
RABBIT_HOST = "rabbit1"
RABBIT_PORT = 5672
