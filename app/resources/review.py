from flask_restful import Resource, request
from ..models.rank_utils import RankUtils
from flask_login import login_required
from flask import session
from . import api

class Review(Resource):
	decorators = [login_required]

	def post(self):
		my_username = session['user_id']
		review_obj = request.get_json()
		rtn = RankUtils().add_review(my_username
							  ,review_obj['item_id']
							  ,review_obj['review_text']
							  ,review_obj['rank'])

		if rtn:
			message = { 'status': 'success', 'message': 'Review added'}
		else:
			message = { 'status': 'failure', 'message': 'Review not added'}

		return message

	def delete(self, item_id):
		my_username = session['user_id']
		rtn = RankUtils().delete_review(my_username, item_id)

		if rtn:
			message = { 'status': 'success', 'message': 'Review deleted' }
		else:
			message = { 'status': 'failure', 'message': 'Review not deleted' }

		return message

api.add_resource(Review, '/review/<int:item_id>', '/review')