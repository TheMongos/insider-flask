#  -*- coding: utf-8 -*-
from flask import send_file
from flask_restful import Resource
from . import api
import os

class Index(Resource):
    def get(self):
        return send_file('static/index.html')

api.add_resource(Index, '/')