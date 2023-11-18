#: import something to access os to write files?
import os
#: Imports flask instance?
from flask import Flask
#: imports db functions
from . import db
#: import auth and blog containing blueprint
from . import auth, blog


#: This is the application factory function
#: Function definition for creating instance of the app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    #: Creates the instance of Flask, __name__ is the current python module
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    #: load config if not testing config is present
    if test_config is None:
        #: Use of different configs for dev, prod and test
        #: Override config in root folder?
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if present
        app.config.from_mapping(test_config)

    # create folder if not present
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a page at /hello which says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #: Runs db init_app before returning app
    db.init_app(app)
    #: Register auth blueprint
    app.register_blueprint(auth.bp)
    #: Register blog bp
    app.register_blueprint(blog.bp)
    #: Associates / to the index name (both blog.index and index)
    app.add_url_rule('/', endpoint='index')
    return app
#: Returns an instance of app

