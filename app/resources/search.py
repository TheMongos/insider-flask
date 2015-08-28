from flask_restful import Resource
from flask_login import login_required
from ..models.user import User
from ..models.item_utils import ItemUtils
from ..models.movie_utils import MovieUtils
from ..models.tv_utils import TvUtils
from . import api

class SearchItem(Resource):
	decorators = [login_required]
	def get(self, item_type, query):
		if item_type == 1:
			rtn_arr = MovieUtils.search_item(query)
		else:
			rtn_arr = TvUtils.search_item(query)
		return rtn_arr

class SearchUser(Resource):
	decorators = [login_required]
	def get(self, query):
		rtn_arr = User.search_user(query)
		return rtn_arr

api.add_resource(SearchItem, '/search/item/<int:item_type>/<string:query>')
api.add_resource(SearchUser, '/search/user/<string:query>')
