from flask_restful import Resource, request
from ..models.movie import MovieItem
from . import api

class Item(Resource):
    def get(self, item_id):
        #TO-DO
        pass

class Movie(Resource):
    def post(self):
    	movie_obj = request.get_json()
        print movie_obj
        signup_status = MovieItem().createMovie(movie_obj)
        print signup_status
        return {'hello' : 'nurse'}

class TV(Resource):
    def post(self):
        signup_obj = request.get_json()
        signup_status = User(signup_obj['username']).register(signup_obj['password']
                                            ,signup_obj['email']
                                            ,signup_obj['first_name']
                                            ,signup_obj['last_name'])
        return {'hello' : 'nurse'}


api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(Movie, '/item/movie')
api.add_resource(TV, '/item/tv')