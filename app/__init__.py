from flask import Flask, abort
from flask_login import LoginManager
from models.user import User

login_manager = LoginManager()

def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = 'pitzkachuckgurgur'
    # TODO: add configuration module
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    login_manager.init_app(app)

    from resources import api_bp
    app.register_blueprint(api_bp)

    return app

@login_manager.user_loader
def load_user(userid):
    return User(userid).find()

@login_manager.unauthorized_handler
def unauth_user():
    return {"message": "Unauthorized", "status": 401}, 401