import os

from dotenv import load_dotenv

# Parse a .env file and then load all the variables found as environment variables.
# If both dotenv_path and stream are None, find_dotenv() is used to find the .env file.
load_dotenv()

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Class Configuration for application
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = True


class DevelopmentConfig(Config):
    """
    :param: Config class
    """
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    host = "localhost"
    port = "27017"
    database_name = "local"
    DEBUG = True
    MONGOALCHEMY_DATABASE_URI = f"mongodb://{host}:{port}/{database_name}" +\
                                os.path.join(basedir, 'flask_boilerplate_main.db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
