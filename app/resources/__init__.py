#  -*- coding: utf-8 -*-
from flask import Blueprint, session, redirect
from flask_restful import Api
from ..models.user import User

api_bp = Blueprint('api', __name__, static_folder='static', static_url_path='/static/')
admin_bp = Blueprint('admin', __name__, static_folder='static', static_url_path='/static/')
api = Api(api_bp)
admin_api = Api(admin_bp)

from . import index, best, item, login, logout, signup, rank, review, search, user, admin, upload

@admin_bp.before_request
def authenticate_admin():
	if session.has_key('user_id'):
		my_username = session['user_id']
		if not User.authenticate_admin(my_username):
			return redirect('/')
	else:
		return redirect('/')

import sys

@api_bp.after_request
def flush_logs(response):
	sys.stdout.flush()
	return response
