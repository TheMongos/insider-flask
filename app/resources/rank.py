from flask_restful import Resource
from . import api

class FollowingRanks(Resource):
    def get(self, item_id):
        return {'following' : 'rank'}

class Rank(Resource):
    def get(self, user_id):
        return {'get' : 'rank'}

    def post(self):
        return {'post' : 'rank'}

api.add_resource(FollowingRanks, '/rank/following/<int:item_id>')
api.add_resource(Rank, '/rank/<int:user_id>', '/rank')