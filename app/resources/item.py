#  -*- coding: utf-8 -*-
from flask_restful import Resource, request
from ..models.item_utils import ItemUtils
from flask_login import login_required
from flask import session
from . import api

class Item(Resource):
    decorators = [login_required]

    def get(self, item_id):
        my_username = session['user_id']
        item = ItemUtils().find(item_id)
        item_ranks = ItemUtils().get_item_ranks(my_username, item_id)
        item_genres = ItemUtils().get_item_genres(item_id)
        message = { 'status': 'success', 'itemDetails': item, 'itemRanks' : item_ranks, 'item_genres' : item_genres}
        return message

class Genres(Resource):
    decorators = [login_required]

    def get(self):
        genres = ItemUtils().get_all_genres()
        return genres

class Movie(Resource):
    decorators = [login_required]

    def post(self):
        movie_obj = request.get_json()
        create_id = ItemUtils().create_item("Movie", movie_obj)
        if create_id:
            return_code = 200
            message = {'status': 'success', 'message': 'item created', 'item_id': create_id}
        else:
            return_code = 409 # 409 = conflict
            message = {'status': 'failure', 'message': 'item already exists.'}

        return message, return_code

class TV(Resource):
    decorators = [login_required]

    def post(self):
        tv_obj = request.get_json()
        create_id = ItemUtils().create_item("TV", tv_obj)
        if create_id:
            return_code = 200
            message = {'status': 'success', 'message': 'item created', 'item_id': create_id}
        else:
            return_code = 409 # 409 = conflict
            message = {'status': 'failure', 'message': 'item already exists.'}

        return message, return_code


api.add_resource(Item, '/item/<int:item_id>')
api.add_resource(Movie, '/item/movie')
api.add_resource(TV, '/item/tv')
api.add_resource(Genres, '/item/genres')