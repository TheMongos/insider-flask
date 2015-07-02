from py2neo import Graph, authenticate

url = 'http://localhost:7474'
username = 'neo4j'
password = 'DavidElad1'

authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')
