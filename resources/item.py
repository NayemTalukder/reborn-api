from flask_restful import Resource, reqparse
from models.item import ItemModel
from models.user import UserModel
from flask_jwt_extended import (jwt_required)

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs a store id"
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        return {'item': item.json()} if item else {'message':'iten not found'}, 200 if item else 404
    
    
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': "An item with name '{}' Already Exists".format(name)}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, **data)
            item.save_to_db()
            return {'item': 'Created'}, 201

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        return item.delete_from_db() if item else {'message': 'Item is Not Found'}, 200 if item else 404
            
    
    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()  
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()   

class Itemlist(Resource):
    def get(self):
        items = ItemModel.get_all_items()
        return items        