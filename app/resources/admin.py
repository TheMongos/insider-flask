from flask_restful import Resource
from ..models.item_utils import ItemUtils
from flask_login import login_required
from flask import session
from . import admin_api

class Admin(Resource):
	decorators = [login_required]
	def get(self):
		return "hi"

	def post(self, item_id, key, value):
		rtn = ItemUtils.update_item(item_id, key, value)
		if rtn:
			message = { 'status': 'success', 'message': 'Item updated successfully'}
		else:
			message = { 'status': 'failure', 'message': 'Item not updated'}

		return message

admin_api.add_resource(Admin, '/', '/updateItem/<int:item_id>/<string:key>/<string:value>')