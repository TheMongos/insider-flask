from flask_restful import Resource
from . import api

class SearchItem(Resource):
    def get(self):
        return {'get': 'item'}

class SearchUser(Resource):
    def get(self):
        return {'get': 'user'}

api.add_resource(SearchItem, '/search/item')
api.add_resource(SearchUser, '/search/user')