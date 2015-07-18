from flask import Flask, abort
from flask_login import LoginManager
from models.user import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'

UPLOAD_FOLDER = '/Users/davidtzoor/Documents/Development/recomate/app/static/images/users/'
ALLOWED_EXTENSIONS = set(['jpg'])

def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = '\xa4\xb5 uzv\x8f\xffyg\xa8<\xc5h\x83\x92Dr)\x81\xddqA5'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # TODO: add configuration module
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    login_manager.init_app(app)

    from resources import api_bp, admin_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

@login_manager.user_loader
def load_user(username):
    return User(username).find()

@login_manager.unauthorized_handler
def unauth_user():
    return {"message": "Unauthorized", "status": 401}, 401
