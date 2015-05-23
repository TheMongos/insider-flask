from flask.ext.login import current_user
from py2neo import Node, Relationship
from . import graph
import time

class Item():
	def __init__(self, title=None, item_id=None, imdb_id=None, language=None, overview=None, poster_path=None, release_date=None, runtime=None, trailer=None):
        self.title = title
        self.item_id = item_id
        self.imdb_id = imdb_id
        self.language = language
        self.overview = overview
        self.poster_path = poster_path
        self.release_date = release_date
        self.runtime = runtime
        self.trailer = trailer

	def find(self, item_type, item_id):
        item = graph.find_one(item_type, "item_id", item_id)
        if item:
            item = Item(**item.properties)
        return item



    def create(self, item_type, item_obj):
        if not self.find() :
            user = Node("Item", "Movie" 
                        ,item_obj)        
            graph.create(user)
            return True
        else:
            return False