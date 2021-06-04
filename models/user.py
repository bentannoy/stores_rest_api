import sqlite3
from db import db


# this class if not a resource because the api cannot receive data into this class
# its a helper that we use to store some data about the user and contains a couple of methods the allow us to easily
# retrieve user objects from the db
# a model is an internal representation of an entity
# a resource is an external representation of an entitu
# so when we deal internally with a User like in security.py we re using the model not the resources

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # we removed the _id from here in this sections because
    # the id is a primary key and it is auto incrementing
    # so whenever we add something the sql engine, sqlite in this case
    # will automatically assign an id for us
    # so we dont have to do it ourselves
    # when the object is created through sqlalchemy it would give us the self.id as well
    # but when we create it we dont need to specify an id, it is automatically created
    #
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'UserModel({self.id}, {self.username}, {self.password})'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

# this is an api
# not a rest api
# it exposes 2 endpoints, 2 methods that are an interface for other parts of the programme
# to interact with the user thing
# we're using this api in the security file, uses this api to communicate with the user and the db
#
