from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Cannot be left blank!',
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200     
        return {'message': 'No item with that name'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'There is already an item like that in DB'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        item.insert()

        return item.json(), 201
        

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not name:
            return {'message': 'no item with that name'}, 401
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close

        return {'message': 'item was deleted successfully'}, 200


    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item:
            try:
                updated_item.update()
            except:
                return {'error': 'There was an error while trying to update'}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {'error': 'There was an error while inserting'}, 500
        
        return updated_item.json(), 200

            
             

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        try:
            query = "SELECT * FROM items"
            results = cursor.execute(query)
            items = []
            for row in results:
                items.append({'name': row[0], 'price': row[1]})
        except:
            return {'message': 'Error while trying to parse data'}, 500
        
        connection.close()

        return {'items': items}, 200
