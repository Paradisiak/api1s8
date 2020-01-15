from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cant be left blank"
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': 'item not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': f"An item {name} already exists"}

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured"}, 500

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']

        else:
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    def get(self):
        return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
    # pythonic way : [item.json() for item in ItemModel.query.all()]
