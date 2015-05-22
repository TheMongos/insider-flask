from flask_restful import Resource
from flask_login import login_required
from . import api

class ThisUser(Resource):
    decorators = [login_required]

    def get(self):
        return {'get': 'user (me)'}

    def post(self, user_follow_id):
        return {'follow': user_follow_id}

class OtherUser(Resource):
    def get(self, user_id):
        return {'get': user_id}

class ThisFollowing(Resource):
    def get(self):
        return {'get': 'following (me)'}

class ThisFollowers(Resource):
    def get(self):
        return {'get': 'followers (me)'}

class OtherFollowing(Resource):
    def get(self, user_id):
        return {'get-following': user_id}

class OtherFollowers(Resource):
    def get(self, user_id):
        return {'get-followers': user_id}

api.add_resource(ThisUser, '/user', '/user/follow/<int:user_follow_id>')
api.add_resource(OtherUser, '/user/<int:user_id>')
api.add_resource(ThisFollowing, '/user/following')
api.add_resource(ThisFollowers, '/user/followers')
api.add_resource(OtherFollowing, '/user/following/<int:user_id>')
api.add_resource(OtherFollowers, '/user/followers/<int:user_id>')