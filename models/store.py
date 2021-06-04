from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # as soon as we create a store model a relationship is created and an object for each time in a database that matches the store id
    # if we have many items this is an expensive operation
    # we can tell sql alchemy not to do that.
    # we can say lay is dynamic and whevever we access the json methof were gonna get a error unless we user all
    # lazy='dynamic' the self.items is no longer a list of items but a query builder that has the ability to look
    # into the items table then we can use .all to retriece all of the items in that table
    #  it also means that every time we call the json methof we have to fo into the table
    # so that is gonna be slower
    # thsi means that we we create the store so we load up all the items
    # and then we can call the kson method many times
    # with lazy every time we call json we have to go into the table so that is slower
    # so here is the trade offf between the speed of creation of the store and speed of calling the json method

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [ item.json() for item in self.items.all()]}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # this will stay as classmethod because it will return a object of item model and not a dictionary
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # select * from items where name=name limit 1

    def save_to_db(self):
        # the sessions in this instance is a collection of objects
        # that we're going to write to the db.
        # we can add multiple objects and write them all at once.
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
