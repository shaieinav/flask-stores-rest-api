from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return { "message": "An Error Occurred While Getting The Store." }, 500

        if store:
            return store.json()
        return { 'message': 'Store Not Found' }, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return { 'message': "A Store With Name '{}' Already Exists.".format(name) }, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return { "message": "An Error Occurred Inserting The Store." }, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return { "message": "Store Deleted." }


class StoreList(Resource):
    def get(self):
        return { 'stores': list(map(lambda x: x.json(), StoreModel.query.all())) } # [store.json() for store in StoreModel.query.all()]
