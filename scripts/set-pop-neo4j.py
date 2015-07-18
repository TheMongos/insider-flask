from py2neo import Graph, Node, Relationship, authenticate
import json
import ast

url = 'http://localhost:7474'
username = 'neo4j'
password = 'DavidElad1'
titles_file = '/home/recomate/tmdb/tmdb_movies.txt'
label = 'Movie'

authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

with open (titles_file, 'r') as f_in:
	id = 1
	for line in f_in:
		try:
			obj = json.loads(line)
		except:
			obj = ast.literal_eval(line)
		if obj['popularity'] < 0.001:
			pop = 0
		else:
			pop = obj['popularity']	
		query = """MATCH (i:Item {{item_id: {0}}})
			   SET i.popularity = {1}""".format(id, pop)
		graph.cypher.execute(query)
		id += 1
