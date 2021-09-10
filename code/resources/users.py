from flask_restful import Resource, reqparse
from models.user import UserModel

db_name = 'data.db'

class UserRegister(Resource):
	
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help='This field cannot be empty',
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help='This field cannot be empty',
	)

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message': 'User already exists with that username'}, 400

		user = UserModel(**data)
		user.save_to_db()
		return {'user': user.json(), 'message': 'User created successfully!!!'}

class User(Resource):

	def get(self, user_id):
		user = UserModel.find_by_id(user_id)
		if user:
			return user.json()
		return {'message': 'User not found'}, 404

	def delete(self, user_id):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {'message': 'User not found'}, 404
		user.delete_from_db()
