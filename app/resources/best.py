from flask_restful import Resource
from . import api

class BestAll(Resource):
    def get(self, category_id):
    	#TO-DO
        pass

class BestFollowing(Resource):
    def get(self, category_id):
    	#TO-DO
        pass

api.add_resource(BestAll, '/best/<int:category_id>')
api.add_resource(BestFollowing, '/best/following/<int:category_id>')