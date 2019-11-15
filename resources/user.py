from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
	create_access_token, 
	create_refresh_token, 
	jwt_refresh_token_required,
	get_jwt_identity,
	fresh_jwt_required,
	jwt_required,
	get_raw_jwt
)
from blacklisting import BLACKLIST

_parser = reqparse.RequestParser()
_parser.add_argument("username", type=str, required=True, help="This field is required")
_parser.add_argument("password", type=str, required=True, help="This field is required")

class User(Resource):

	@jwt_required
	def get(cls):
		data = _parser.parse_args()
		username = data['username']
		user = UserModel.find_by_username(username)
		if user:
			return user.json()
		return {"message" : "user not found"}

	@fresh_jwt_required
	def put(self):
		data = _parser.parse_args()
		username = data['username']
		user = UserModel.find_by_username(username)
		if user:
			user.password = data['password']
			return user.json()
		return {"message" : "user not found"}

class UserRegistry(Resource):
	
	@classmethod
	def post(cls):
		data = _parser.parse_args()
		username  = data['username']
		user = UserModel.find_by_username(username)
		if user:
			return {"message" : "username is taken"}
		user = UserModel(username, data['password'])
		user.save_to_db()
		return user.json()

class UserLogin(Resource):

	@classmethod
	def post(cls):
		data = _parser.parse_args()
		username = data['username']
		user = UserModel.find_by_username(username)
		if user and safe_str_cmp(user.password, data['password']):
			access_token = create_access_token(identity=user.id, fresh=True)
			refresh_token = create_refresh_token(user.id)
			return {
				"access_token" : access_token,
				"refresh_token" : refresh_token
				}
		return {"message" : "Invalid credential"}, 401
		


class TokenRefresh(Resource):

	@jwt_refresh_token_required
	def post(self):
		user_id = get_jwt_identity()
		access_token = create_access_token(identity=user_id, fresh=False)
		return {"access_token" : access_token}, 200
	

class UserLogout(Resource):
	@jwt_required
	def post(self):
		access_id = get_raw_jwt()['jti']
		BLACKLIST.add(access_id)
		return {"message" : "Logout successful"}
				


