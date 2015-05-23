from flask_restful import Resource
from flask_login import login_required
from flask import session
from ..models.user import User
from . import api

class ThisUser(Resource):
    decorators = [login_required]

    def get(self):
        my_username = session['user_id']
        user = User(my_username).getUser(my_username)
        if len(user) != 0:
            return_code = 200
            message = { 'status': 'success', 'user': user}
        else:
            return_code = 401
            message = { 'status': 'failure', 'message': 'user not found!'}

        return message, return_code

    def post(self, user_follow_username):
        my_username = session['user_id']
        res = User(my_username).addUserFollowing(user_follow_username)
        if res:
            return_code = 200
            message = { 'status': 'success', 'message': 'you are now following ' + user_follow_username}
        else:
            return_code = 200
            message = { 'status': 'failure', 'message': 'you are already following' }

        return {'follow': user_follow_username}

class OtherUser(Resource):
    decorators = [login_required]

    def get(self, username):
        my_username = session['user_id']
        user = User(my_username).getUser(username)
        if len(user) != 0:
            return_code = 200
            message = { 'status': 'success', 'user': user}
        else:
            return_code = 401
            message = { 'status': 'failure', 'message': 'user not found!'}

        return message, return_code

# class ThisFollowing(Resource):
#     def get(self):
#         my_username = session['user_id']
#         followingArr = User(my_username).getUserFollowing()
#         return followingArr

# class ThisFollowers(Resource):
#     def get(self):
#         my_username = session['user_id']
#         followersArr = User(my_username).getUserFollowers()
#         return followersArr

class Following(Resource):
    decorators = [login_required]

    def get(self, username):
        followingArr = User(username).getUserFollowing()
        return followingArr

class Followers(Resource):
    decorators = [login_required]

    def get(self, username):
        followersArr = User(username).getUserFollowers()
        return followersArr

api.add_resource(ThisUser, '/user', '/user/follow/<string:user_follow_username>')
api.add_resource(OtherUser, '/user/<string:username>')
# api.add_resource(ThisFollowing, '/user/following')
# api.add_resource(ThisFollowers, '/user/followers')
api.add_resource(Following, '/user/following/<string:username>')
api.add_resource(Followers, '/user/followers/<string:username>')