from flask_restful import Resource
from . import api

class Item(Resource):
    def get(self, item_id):
        pass

    def post(self):
        return {'hello' : 'nurse'}

api.add_resource(Item, '/item/<int:item_id>', '/item')