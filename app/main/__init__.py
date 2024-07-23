import os

from flask import Flask


def create_app():
    """
    :return: It's returns the application server to run along with desired configuration.
    """
    # create and configure the app
    #  Flask instance. __name__ current Python module.
    #  The app needs to know where it's located to set up some paths, and __name__ is a convenient way.
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
    # app.secret_key = "secret key"
    app.config['ENV'] = 'Development'
    app.config['AUTO_RELOADER'] = True
    app.config['DEBUG'] = True
    try:
        # creating instance folder before application starts.
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app
