from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This Field Cannot Be Left Blank!'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every Item Needs a Store ID.'
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return { "message": "An Error Occurred While Getting The Item." }, 500

        if item:
            return item.json()
        return { 'message': 'Item Not Found' }, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return { 'message': "An Item With Name '{}' Already Exists.".format(name) }, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return { "message": "An Error Occurred Inserting The Item." }, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return { "message": "Item Deleted." }

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return { 'items': list(map(lambda x: x.json(), ItemModel.query.all())) } # [item.json() for item in ItemModel.query.all()]
