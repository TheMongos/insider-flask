from py2neo import Node
from . import graph
from . import SQL_DB
import sqlite3


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
                , round(100 * avg(r.rank)) / 100 as totalAvg
                , r2.rank as rank
                , r2.review_text as review_text
                , count(distinct u3) as followingCount
                , round(100 * avg(r3.rank)) / 100 as followingAvg""".format(username, item_id)
        print query
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            keys = queryRes.columns
            values = [value for value in queryRes[0]]
            item_ranks = dict(zip(keys, values))
        else:
            item_ranks = {}
        return item_ranks

    def get_item_genres(self, item_id):
        query = """MATCH (i:Item {{item_id: {0}}})-[:OF_GENRE]->(g:Genre)
                RETURN collect(g.name)""".format(item_id)
        query_res = graph.cypher.execute(query)
        if len(query_res) != 0:
            genres = query_res[0][0]
        else:
            genres = []
        return genres

    def create_item(self, label, item_obj):
        new_id = ItemUtils.get_new_id()
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
        print query
        new_id = graph.cypher.execute(query)[0][0]

        return new_id

    @staticmethod
    def search_item(query):
        item_ids_str = ItemUtils.search_item_in_sql(query)
        query = """MATCH (i:Item)
                WHERE i.item_id IN [{0}]
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.release_date, '-')[0] as year
                      ,filter(x in labels(i) WHERE x <> 'Item')[0] AS label
                LIMIT 25""".format(item_ids_str)
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
    def get_best(label, genre=None):
        where_clause = ''
        if genre:
            where_clause = ', (i)-[:OF_GENRE]->(g1:Genre) WHERE g1.name = "{0}"'.format(genre)

        query = """MATCH (u:User)-[r:RANKED]->(i:{0})-[:OF_GENRE]->(g:Genre) {1}
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.release_date, '-')[0] AS year
                      ,COALESCE(round(100 * AVG(r.rank)) / 100, 0) as avg
                      ,COLLECT(distinct g.name) as genres
                ORDER BY avg DESC 
                LIMIT 25""".format(label, where_clause)
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
    def get_following_best(username, label, genre=None):
        where_clause = ''
        if genre:
            where_clause = ', (i)-[:OF_GENRE]->(g1:Genre) WHERE g1.name = "{0}"'.format(genre)

        query = """MATCH (u1:User {{username: '{0}'}})-[:FOLLOWS]->(u:User)-[r:RANKED]->(i:{1})-[:OF_GENRE]->(g:Genre) {2}
                RETURN i.item_id AS item_id
                      ,i.title AS title
                      ,i.poster_path AS poster_path
                      ,split(i.release_date, '-')[0] AS year
                      ,COALESCE(round(100 * AVG(r.rank)) / 100, 0) as avg
                      ,COLLECT(distinct g.name) as genres
                ORDER BY avg DESC 
                LIMIT 25""".format(username, label, where_clause)
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

    @staticmethod
    def get_all_genres():
        query = 'MATCH (g:Genre) RETURN COLLECT(g.name)'
        query_res = graph.cypher.execute(query)
        if len(query_res) != 0:
            genres = query_res[0][0]
        else:
            genres = []
        return genres

    @staticmethod
    def search_item_in_sql(query):
        query = """SELECT item_id
                FROM Title
                WHERE title LIKE '%{0}%'
                LIMIT 25""".format(query)

        print query
        connection = sqlite3.connect(SQL_DB)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(str(row[0]))
        print result
        return ','.join(result)
