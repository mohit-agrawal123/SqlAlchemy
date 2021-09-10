from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return {'store': store.json()}
		return {'message': 'Store not found'}, 400

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': 'Store already exists with that name'}, 400
		store = StoreModel(name)
		try:
			store.save_to_db()
		except Exception:
			return {'message': 'An error occured while creating the store'}, 500
		return store.json()

	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
			return {'message': 'Store deleted'}
		return {'message': 'Store not found'}, 400

class StoreList(Resource):
	def get(self):
		return {'stores': [store.json() for store in StoreModel.find_all()]}
