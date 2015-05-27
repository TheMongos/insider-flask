from py2neo import Node
from . import graph



class ItemUtils():
    # def __init__(self, label=None, item_id=None, title=None, tmdb_id=None, imdb_id=None, language=None, overview=None, poster_path=None, release_date=None, runtime=None, trailer=None):
    #     self.label = label
    #     self.item_id = item_id
    #     self.title = title
    #     self.tmdb_id = tmdb_id
    #     self.imdb_id = imdb_id
    #     self.language = language
    #     self.overview = overview
    #     self.poster_path = poster_path
    #     self.release_date = release_date
    #     self.runtime = runtime
    #     self.trailer = trailer

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
        print query
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            keys = queryRes.columns
            values = [value for value in queryRes[0]]
            item_ranks = dict(zip(keys, values))
        else:
            item_ranks = {}
        print item_ranks
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
