import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    stores = db.relationship('StoreModel') # normally you would need to use joins,
    # but sql alchemy does that for us
    # with this line
    # now every item model has a property store which matches this store id
    #

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'store_id': self.store_id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # this will stay as classmethod because it will return a obkect of item model and not a dictionary
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # select * from items where name=name limit 1

    # with sql alchemy the insert for both update and and insert
    # when we retrieve an object from the db that has an id then we can change the objects name
    # and all we can do is we have to add it to the sessions and commit it again
    # and sql alchemy will do an update instead of an insert
    # so this methods is for both update and insert
    #
    def save_to_db(self):
        # the sessions in this instance is a collection of objects
        # that we're going to write to the db.
        # we can add multiple objects and write them all at once.
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
