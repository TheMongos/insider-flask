from flask.ext.login import UserMixin, current_user
from passlib.hash import bcrypt
from py2neo import Node, Relationship
from . import graph

class User(UserMixin):
    def __init__(self, username, password=None, first_name=None, last_name=None, email=None, role=None, authenticated=False):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
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
