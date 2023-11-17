import os
from flask import Flask
'''Imports flask instance?'''


def create_app(test_config=None):
    #: Function definition for creating instance of the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load config if not testing config is present
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if present
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a page at /hello which says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
#: Returns an instance of app
