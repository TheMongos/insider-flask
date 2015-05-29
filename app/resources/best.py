from flask_restful import Resource
from flask_login import login_required
from ..models.item_utils import ItemUtils
from flask import session
from . import api

class BestAll(Resource):
	decorators = [login_required]
	def get(self, label):
		rtn_arr = ItemUtils.get_best(label)
		print rtn_arr
		return rtn_arr

class BestFollowing(Resource):
	decorators = [login_required]	
	def get(self, label):
		my_username = session['user_id']
		rtn_arr = ItemUtils.get_following_best(my_username, label)
		print rtn_arr
		return rtn_arr

api.add_resource(BestAll, '/best/<string:label>')
api.add_resource(BestFollowing, '/best/following/<string:label>')