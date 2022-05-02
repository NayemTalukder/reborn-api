from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt_extended import (jwt_required)

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        return {'store': store.json()} if store else {'message': 'store not found'}, 200 if store else 404        
   
    
    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': 'store already exits'}, 400
        else:   
            store = StoreModel(name)
            store.save_to_db()
            return {'store': 'Created'}, 201

    @jwt_required
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store Deleted'}
        else:
            return {'message': 'Store is Not Found'}  

class Storelist(Resource):
    def get(self):
        stores = StoreModel.get_all_stores()
        return stores        