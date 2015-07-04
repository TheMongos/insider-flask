from py2neo import Graph, authenticate

url = 'http://localhost:7474'
username = 'neo4j'
password = 'DavidElad1'

authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

#graph constraints
nodes = [
    ('Item', 'tmdb_id'),
    ('User', 'username')
]

for label, property in nodes:
    try:
        graph.schema.create_uniqueness_constraint(label, property)
    except:
        continue