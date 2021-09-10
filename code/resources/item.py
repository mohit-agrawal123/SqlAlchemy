from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

db_name = 'data.db'

class Item(Resource):

	parser = reqparse.RequestParser() # This will update only the keys which we pass as arguement.
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be blank!"
	)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="This field cannot be blank!"
	)

	@jwt_required() # Now this api needs authentication token to get called.
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'Item not found'}, 400 # 404 will return as status code.

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': 'Item already exists'}, 404 # 404 will return as status code.
		data = Item.parser.parse_args()
		item = ItemModel(name, **data) # **data = data['price'], data['store_id']
		item.save_to_db()

		return item.json()

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item is None:
			return {'message': 'Item not found'}, 404 # 404 will return as status code.

		item.delete_from_db()

	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)
		if item is None:
			item = ItemModel(name, **data)
		else:		
			item.price = data['price']
		item.save_to_db()
		return item.json()

class ItemList(Resource):
	def get(self):
		items = ItemModel.find_all()
		return {'items': [item.json() for item in items]}
