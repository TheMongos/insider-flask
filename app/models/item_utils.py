from py2neo import Node
from . import graph



class ItemUtils():

    def find(self, item_id):
        item = graph.find_one("Item", "item_id", item_id)
        if item:
            item.properties['label'] = item.get_labels()
            item = dict(item.properties)
        return item

    def get_item_ranks(self, username, item_id):
        query = """MATCH (u:User {{username: '{0}'}}), (i:Item {{item_id: {1}}})
                OPTIONAL MATCH (i)<-[r:RANKED]-(u2:User)
                OPTIONAL MATCH (u)-[r2:RANKED]->(i)
                OPTIONAL MATCH (u)-[:FOLLOWS]->(u3:User)-[r3:RANKED]->(i)
                RETURN count(distinct u2) as totalCount
                , avg(r.rank) as totalAvg
                , r2.rank as rank
                , r2.review_text as review_text
                , count(distinct u3) as followingCount
                , avg(r3.rank) as followingAvg""".format(username, item_id)
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            keys = queryRes.columns
            values = [value for value in queryRes[0]]
            item_ranks = dict(zip(keys, values))
        else:
            item_ranks = {}
        return item_ranks

    def create_item(self, label, item_obj):
        new_id = get_new_id()
        item_obj['item_id'] = new_id
        item = Node("Item", label, **item_obj)
        rtn = graph.create(item)
        return new_id

    @staticmethod
    def get_new_id():
        query = """MERGE (nid:ItemIncremental)
                ON CREATE SET nid.count = 1
                ON MATCH SET nid.count = nid.count + 1
                RETURN nid.count"""
        new_id = graph.cypher.execute(query)[0][0]

        return new_id

    @staticmethod
    def search_item(query):
        query = """MATCH (i:Item)
                WHERE i.title =~ "(?i){0}.*"
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.release_date, '-')[0] as year
                      ,filter(x in labels(i) WHERE x <> 'Item')[0] AS label
                LIMIT 25""".format(query)
        queryRes = graph.cypher.execute(query)
        rtn_arr = []
        for i in range(len(queryRes)):
            keys = queryRes.columns
            values = [value for value in queryRes[i]]
            rank = dict(zip(keys, values))
            rtn_arr.append(rank)
        return rtn_arr

    @staticmethod
    def get_best(label):
        query = """MATCH (u:User)-[r:RANKED]->(i:{0})
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.release_date, '-')[0] AS year
                      ,COALESCE(AVG(r.rank), 0) as avg
                ORDER BY avg DESC 
                LIMIT 25""".format(label)
        print query
        queryRes = graph.cypher.execute(query)
        rtn_arr = []
        for i in range(len(queryRes)):
            keys = queryRes.columns
            values = [value for value in queryRes[i]]
            rank = dict(zip(keys, values))
            rtn_arr.append(rank)
        return rtn_arr

    @staticmethod
    def get_following_best(username, label):
        query = """MATCH (u1:User {{username: '{0}'}})-[:FOLLOWS]->(u:User)-[r:RANKED]->(i:{1})
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.release_date, '-')[0] AS year
                      ,COALESCE(AVG(r.rank), 0) as avg
                ORDER BY avg DESC 
                LIMIT 25""".format(username, label)
        print query
        queryRes = graph.cypher.execute(query)
        rtn_arr = []
        for i in range(len(queryRes)):
            keys = queryRes.columns
            values = [value for value in queryRes[i]]
            rank = dict(zip(keys, values))
            rtn_arr.append(rank)
        return rtn_arr

    @staticmethod
    def update_item(item_id, key, value):
        query = """MATCH (i:Item {{item_id: {0}}})
                SET i.{1} = '{2}' 
                RETURN i.{1}""".format(item_id, key, value)
        print query
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            return True
        else:
            return False