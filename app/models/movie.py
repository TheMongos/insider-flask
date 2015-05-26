from flask.ext.login import current_user
from py2neo import Node, Relationship
from . import graph
import time


class MovieItem():
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

    def find(self, item_id):
        movie = graph.find_one("Movie", "item_id", item_id)
        if movie:
            movie = MovieItem(**movie.properties)
        return movie

    def createMovie(self, item_obj):
        if not self.find(item_obj['item_id']):
            movie = Node("Item", "Movie", **item_obj)        
            rtn = graph.create(movie)
            print rtn
            return True
        else:
            return False