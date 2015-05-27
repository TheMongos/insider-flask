from flask_restful import Resource
from ..models.rank_utils import RankUtils
from flask_login import login_required
from flask import session
from . import api

class FollowingRanks(Resource):
	decorators = [login_required]
	def get(self, item_id):
		my_username = session['user_id']
		rtn_arr = RankUtils().get_following_ranks(my_username, item_id)
		return rtn_arr

class Rank(Resource):
	decorators = [login_required]

	def get(self, username):
		return RankUtils().get_user_ranks(username)


	def post(self, item_id, rank):
		my_username = session['user_id']
		if RankUtils().add_rank(my_username, item_id, rank):
			message = { 'status': 'success', 'message': 'Rank added'}
		else:
			message = { 'status': 'failure', 'message': 'Rank not added'}

		return message

api.add_resource(FollowingRanks, '/rank/following/<int:item_id>')
api.add_resource(Rank, '/rank', '/rank/<string:username>', '/rank/<int:item_id>/<int:rank>')