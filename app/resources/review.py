from flask_restful import Resource
from . import api

class Review(Resource):
    def get(self, review_id):
        return {'get': 'review'}

    def post(self):
        return {'post': 'review'}

    def delete(self):
        return {'delete': 'review'}

api.add_resource(Review, '/review/<int:review_id>', '/review')