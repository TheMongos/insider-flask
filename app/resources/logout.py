from flask_restful import Resource
from flask_login import logout_user, login_required, current_user
from . import api
from ..models.user import User

class Logout(Resource):

    decorators = [login_required]

    def post(self):
        User(current_user.username).logout()
        logout_user()
        #TO-DO
        return {'logout' : 'logout'}

api.add_resource(Logout, '/logout')