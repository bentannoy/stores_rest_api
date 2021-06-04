from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'A store with name "{}" already exists.'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return store.json(), 201

    def delete(self, name):
        if not StoreModel.find_by_name(name):
            return {'message': 'A store with name "{}" does not exist.'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.delete_fromd_db()
        except:
            return {'message': 'An error occurred deleting the item.'}, 500

        return {'message': 'Item deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.find_all()]}

