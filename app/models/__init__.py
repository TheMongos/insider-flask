#  -*- coding: utf-8 -*-
from py2neo import Graph, authenticate

url = 'http://localhost:7474'
username = 'neo4j'
password = 'DavidElad1'

SQL_DB = "db/search_title.db"

authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

# graph constraints
nodes = [
    ('Movie', 'tmdb_id'),
    ('TV', 'tmdb_id'),
    ('User', 'username')
]

for label, property in nodes:
    try:
        graph.schema.create_uniqueness_constraint(label, property)
    except:
        continue

# graph indexes
nodes = [
    ('Item', 'item_id')
]

for label, property in nodes:
    try:
        graph.schema.create_index(label, property)
    except:
        continue
