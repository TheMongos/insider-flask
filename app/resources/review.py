from flask_restful import Resource
from . import api

class Review(Resource):
    def get(self, review_id):
    	#TO-DO
        return {'get': 'review'}

    def post(self):
    	#TO-DO
        return {'post': 'review'}

    def delete(self):
    	#TO-DO
        return {'delete': 'review'}

api.add_resource(Review, '/review/<int:review_id>', '/review')