from flask.ext.login import UserMixin, current_user
from passlib.hash import bcrypt
from py2neo import Node, Relationship
from . import graph
import time

class User(UserMixin):
    def __init__(self, username, password=None, first_name=None, last_name=None, email=None, role=None, created_ts=None, authenticated=False):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.created_ts = created_ts
        self.authenticated = authenticated

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return current_user.is_authenticated

    def find(self):
        user = graph.find_one("User", "username", self.username)
        if user:
            user = User(**user.properties)
        return user

    def find_by_email(self, email):
        user = graph.find_one("User", "email", email)
        if user:
            user = User(**user.properties)
        return user

    def login(self):
        self.authenticated = True
        user = graph.find_one("User", "username", self.username)
        user['authenticated'] = True
        graph.push(user)

    def logout(self):
        user = graph.find_one("User", "username", self.username)
        user['authenticated'] = False
        graph.push(user)

    def register(self, password, email, first_name, last_name, role='user'):
        if not self.find() and not self.find_by_email(email):
            user = Node("User" 
                        ,username=self.username
                        ,password=bcrypt.encrypt(password)
                        ,first_name=first_name
                        ,last_name=last_name
                        ,email=email
                        ,role=role
                        ,created_ts=int(time.time())
                        ,authenticated=False)
                        
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user.password)
        else:
            return False

    def addUserFollowing(self, user_follow_username):
        query = """MATCH (u1:User {{username: '{0}'}}), (u2:User {{username: '{1}'}}) 
        CREATE UNIQUE (u1)-[r:FOLLOWS]->(u2) 
        RETURN r""".format(self.username, user_follow_username)
        queryRes = graph.cypher.execute(query)
        
        if len(queryRes):
            return True
        else:
            return False

    def getUser(self, username):
        query = """MATCH (u1:User {{username: '{0}'}})
        OPTIONAL MATCH (u1)<-[r:FOLLOWS]-(u2:User {{username: '{1}'}})
        OPTIONAL MATCH (u1)-[:FOLLOWS]->(u3:User)
        OPTIONAL MATCH (u4:User)-[:FOLLOWS]->(u1)
        RETURN u1.username as username,
        u1.first_name as first_name,
        u1.role as role,
        u1.last_name as last_name,
        r IS NOT NULL as isFollowing, 
        count(u3) as userFollowingCount, 
        count(u4) as userFollowersCount, 
        '{0}' = '{1}' as isMyAccount""".format(username, self.username)
        queryRes = graph.cypher.execute(query)
        if len(queryRes) != 0:
            keys = queryRes.columns
            values = [value for value in queryRes[0]]
            user = dict(zip(keys, values))
        else:
            user = {}

        return user

    def getUserFollowing(self):
        query = """MATCH (u1:User {{username: '{0}'}})-[:FOLLOWS]->(u2:User) 
        RETURN u2.username as username""".format(self.username)
        query_res = graph.cypher.execute(query)
        res_arr = []
        for i in range(len(query_res)):
            res_arr.append(query_res[i]['username'])
        return res_arr

    def getUserFollowers(self):
        query = """MATCH (u1:User {{username: '{0}'}})<-[:FOLLOWS]-(u2:User) 
        RETURN u2.username as username""".format(self.username)
        query_res = graph.cypher.execute(query)
        res_arr = []
        for i in range(len(query_res)):
            res_arr.append(query_res[i]['username'])
        return res_arr

    @staticmethod
    def search_user(query):
        query = """MATCH (u:User) 
                WHERE u.username =~ "(?i){0}.*" 
                RETURN u.username as username""".format(query)
        query_res = graph.cypher.execute(query)
        res_arr = []
        for i in range(len(query_res)):
            res_arr.append(query_res[i]['username'])
        return res_arr

    @staticmethod
    def authenticate_admin(username):
        user = User(username).find()
        if user.role == 'admin':
            return True
        else:
            return False

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
