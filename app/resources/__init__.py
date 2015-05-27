from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__, static_folder='static', static_url_path='/static/')
api = Api(api_bp)

from . import index, best, item, login, logout, signup, rank, review, search, user