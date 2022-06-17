from queue import Empty
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item_model import ItemModel

# this is a resoure file, here we want to keep that things, which interact with API direvtly
class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',   # this will be used , when we get data through headers from API call, 
        type=float,                #so we want to confirm that data as arguments       
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args() # used to parse data coming from API request

        item = {'name': name, 'price': data['price']}

        try:
           # ItemModel.insert(item)
           item1 = ItemModel(item['name'], item['price'])
           item1.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item

    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        else:    
            return {'message': "An item with name '{}' doesnt exists.".format(name)}

        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #query = "DELETE FROM items WHERE name=?"
        #cursor.execute(query, (name,))
        #connection.commit()
        #connection.close()
        
        

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        item.save_to_db()
        return item.json()

        # #if item is None:
        #     try:
        #         ItemModel.insert(updated_item)
        #     except:
        #         return {"message": "An error occurred inserting the item."}
        # else:
        #     try:
        #         ItemModel.update(updated_item)
        #     except:
        #         return {"message": "An error occurred updating the item."}
        # return updated_item


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):

        queryResult = ItemModel.query.all()
        print(f"{queryResult}, Itemlist wala")
        items = []
        for item in queryResult:
          print(item)  
          items.append(item.json())
        
        return {'items': items}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # connection.close()

        # return {'items': items}