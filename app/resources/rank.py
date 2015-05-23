from flask_restful import Resource
from . import api

class FollowingRanks(Resource):
    def get(self, item_id):
    	#TO-DO
        return {'following' : 'rank'}

class Rank(Resource):
    def get(self, username):
    	#TO-DO
        return {'get' : 'rank'}

    def post(self):
    	#TO-DO
        return {'post' : 'rank'}

api.add_resource(FollowingRanks, '/rank/following/<int:item_id>')
api.add_resource(Rank, '/rank/<string:username>', '/rank')