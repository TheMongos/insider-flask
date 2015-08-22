from py2neo import Graph, Node, Relationship, authenticate
import json
import ast
import sqlite3
# import requests

url = 'http://localhost:7474'
username = 'neo4j'
password = 'DavidElad1'
titles_file = '/home/recomate/tmdb/tmdb_tv.txt.new'
label = 'TV'

authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

con = sqlite3.connect('../db/search_title.db')
cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS Title (title TEXT, item_id INT, poster_path TEXT, year INT)")
# cur.execute("CREATE INDEX IF NOT EXISTS title_index ON Title (title)")

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
        no_genre_counter = 0
        for line in f_in:
            try:
                obj = json.loads(line)
            except:
                obj = ast.literal_eval(line)

            id = get_new_id()

            item = Node('Item', label, item_id = id, title = obj['name'], tmdb_id = obj['id'], language = obj['original_language'], overview = obj['overview'], poster_path = obj['poster_path'], first_air_date = obj['first_air_date'], last_air_date = obj['last_air_date'], status = obj['status'], number_of_seasons = obj['number_of_seasons'], popularity = obj['popularity'])
	    
	    if obj['first_air_date']:
		first_air = obj['first_air_date'].split('-')[0]
	    else:
		first_air = ''
            if obj['last_air_date']:
                last_air = obj['last_air_date'].split('-')[0]
	    else:
 		last_air = ''

	    if obj['status'] == 'Ended':
	    	year = "{0}-{1}".format(first_air, last_air) 
	    else:
		year = "{0}-".format(first_air)

            cur.execute("INSERT INTO Title VALUES(?, ?, ?, ?, ?, ?)", (obj['name'], id, obj['poster_path'], year, obj['popularity'], 'TV'))

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
            #if counter == 1:
            #    break

cur.close()
con.close()
print counter
