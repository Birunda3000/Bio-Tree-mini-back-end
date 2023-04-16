import os.path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    JWT_EXP = 10
    ACTIVATION_EXP_SECONDS = 100000
    # Remove additional message on 404 responses
    RESTX_ERROR_404_HELP = False
    # Swagger
    RESTX_MASK_SWAGGER = False
    # Email
    ''' 
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "smart.hospital@uece.br"
    MAIL_PASSWORD = "uwhlwnievltsujkx"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    '''
    # Pagination
    CONTENT_PER_PAGE = [10, 20, 30, 50, 100]
    DEFAULT_CONTENT_PER_PAGE = CONTENT_PER_PAGE[0]
    # The maximum file size for upload
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 megas

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "storage.db")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "development"
    HOST = "localhost"

    # uncomment the line below to see SQLALCHEMY queries
    # SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "storage.db")
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "testing"


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
)

_env_name = os.environ.get("ENV_NAME")
_env_name = _env_name if _env_name is not None else "dev"
app_config = config_by_name[_env_name]