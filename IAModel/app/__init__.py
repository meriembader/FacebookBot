# app/__init__.py

# third-party imports
import importlib
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


import config
from app.datatraining import chatbot
# db variable initialization
db = SQLAlchemy()
login_manager= LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config.DevelopmentConfig)
    app.config.from_pyfile('config.py')
    Bootstrap(app)
    db.init_app(app)
    ####trainingdata-chatbot
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    @app.route('/flask/<string:msg>', methods=['GET','POST'])
    def index(msg):
        msgres=chatbot.trainingchat(msg)
        return jsonify({'text': msgres})
    ####authertification avec flasl-login
    login_manager.init_app(app)
    login_manager.login_message="you must be logged in to access this page"
    login_manager.login_view ="auth_login"
    ####migrations
    migrate = Migrate(app, db)
    from app import models

    ###bleuprints
    from .admin  import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
     ####tyto
    from .enseignant import enseignant as enseignant_bleuprint
    app.register_blueprint(enseignant_bleuprint)

    return app

