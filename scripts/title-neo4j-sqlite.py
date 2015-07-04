from py2neo import Graph, Node, Relationship, authenticate
import json
import ast
import sqlite3
# import requests

url = 'http://localhost:7474'
username = 'neo4j'
password = 'DavidElad1'
titles_file = '/home/recomate/tmdb/tmdb_movies.txt'
label = 'Movie'

authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

con = sqlite3.connect('../db/search_title.db')
cur = con.cursor()
cur.execute("CREATE TABLE Title (title TEXT, item_id INT, poster_path TEXT, year INT)")
cur.execute("CREATE INDEX title_index ON Title (title)")

def get_new_id():
    query = """MERGE (nid:ItemIncremental)
            ON CREATE SET nid.count = 1
            ON MATCH SET nid.count = nid.count + 1
            RETURN nid.count"""
    new_id = graph.cypher.execute(query)[0][0]

    return new_id

# graph = Graph()
genres = graph.find('Genre')
genre_dict = {}

for genre in genres:
    genre_dict[genre.properties['name']] = genre

with con:
    with open (titles_file, 'r') as f_in:
        counter = 0
        more_than_one = 0
        no_genre_counter = 0
        for line in f_in:
            try:
                obj = json.loads(line)
            except:
                obj = ast.literal_eval(line)
            trailer_link = ''
            # if len(obj['genres']) == 0:
            try:
                if obj['trailers']['youtube'][0]['source']:
                    trailer_link = obj['trailers']['youtube'][0]['source']
            except:
                pass

            # add item to server with request
            # item = json.dumps(item)
            # headers = {'Content-type' : 'application/json'}
            # requests.post("http://localhost:5000/item/movie", data=item, headers=headers)

            id = get_new_id()

            if trailer_link:
                item = Node('Item', label, item_id = id, title = obj['title'], tmdb_id = obj['id'], imdb_id = obj['imdb_id'], language = obj['original_language'], overview = obj['overview'], poster_path = obj['poster_path'], release_date = obj['release_date'], runtime = obj['runtime'], trailer = trailer_link)
            else:
                item = Node('Item', label, item_id = id, title = obj['title'], tmdb_id = obj['id'], imdb_id = obj['imdb_id'], language = obj['original_language'], overview = obj['overview'], poster_path = obj['poster_path'], release_date = obj['release_date'], runtime = obj['runtime'])

            cur.execute("INSERT INTO Title VALUES(?, ?, ?, ?)", (obj['title'], id, obj['poster_path'], obj['release_date'].split('-')[0]))
            # no_genre_counter = no_genre_counter + 1

            # add item to server with create
            try:
                graph.create(item)
            except Exception as e:
                print e.message
                continue

            for genre in obj['genres']:
                if genre['name'] not in genre_dict:
                    new_genre = Node("Genre", tmdb_id = genre['id'], name = genre['name'])
                    graph.create(new_genre)
                    genre_dict[genre['name']] = new_genre
                genre_rel = Relationship(item, 'OF_GENRE', genre_dict[genre['name']])
                graph.create_unique(genre_rel)

            # print json.dumps(obj, indent=4, sort_keys=True)

            counter = counter + 1
            # for debug
            #if counter == 100:
            #    break

cur.close()
con.close()
print counter
