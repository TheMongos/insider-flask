from py2neo import Node
from . import graph

class RankUtils():
    def add_rank(self, username, item_id, rank):
        query = """MATCH (u:User {{username: '{0}'}}), (i:Item {{item_id: {1}}})
			        CREATE UNIQUE (u)-[r:RANKED]->(i)
			        SET r.rank = {2}
			        ,r.ts = timestamp()
			        RETURN r.rank""".format(username, item_id, rank)
        print query
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            return True
        else:
            return False

    def get_user_ranks(self, username):
        query = """MATCH (u:User {{username: '{0}'}})-[r:RANKED]->(i:Item)
                    RETURN r.rank as rank
                    , r.review_text as review_text
                    , i.item_id as item_id
                    , i.title as title
                    , i.poster_path as poster_path""".format(username)
        print query
        queryRes = graph.cypher.execute(query)
        rtn_arr = []
        for i in range(len(queryRes)):
            keys = queryRes.columns
            values = [value for value in queryRes[i]]
            rank = dict(zip(keys, values))
            rtn_arr.append(rank)
        return rtn_arr

    def get_following_ranks(self, username, item_id):
        query = """MATCH (u:User {{username: '{0}'}})-[:FOLLOWS]->(u1:User)-[r:RANKED]->(i:Item {{item_id: {1}}})
                    RETURN r.rank as rank
                    , r.review_text as review_text
                    , u1.username as username""".format(username, item_id)
        print query
        queryRes = graph.cypher.execute(query)
        rtn_arr = []
        for i in range(len(queryRes)):
            keys = queryRes.columns
            values = [value for value in queryRes[i]]
            rank = dict(zip(keys, values))
            rtn_arr.append(rank)
        return rtn_arr

    def add_review(self, username, item_id, review_text, rank):
        query = """MATCH (u:User {{username: '{0}'}}), (i:Item {{item_id: {1}}})
                    CREATE UNIQUE (u)-[r:RANKED]->(i)
                    SET r.rank = {2}, r.review_text = '{3}'
                    ,r.ts = timestamp()
                    RETURN r.rank""".format(username, item_id, rank, review_text)
        print query
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            return True
        else:
            return False

    def delete_review(self, username, item_id):
        query = """MATCH (u:User {{username: '{0}'}})-[r:RANKED]->(i:Item {{item_id: {1}}})
                    REMOVE r.review_text
                    RETURN r.rank""".format(username, item_id)
        print query
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            return True
        else:
            return False
