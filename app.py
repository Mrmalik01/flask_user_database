from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from resources.user import User, UserRegistry, UserLogin, TokenRefresh, UserLogout
from database import db
from blacklisting import BLACKLIST
app = Flask(__name__)

api = Api(app)

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "example"

class Homepage(Resource):
	@classmethod
	def get(self):
		return "<h1> Service working </h1>"

@jwt.expired_token_loader
def expired_token_callback():
	return jsonify({
		"description" : "token is expired",
		"error"  : "Token expired"
		}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
	return jsonify({ "description" : "Passed access token is invalid", "error" : "Invalid token"})

@jwt.unauthorized_loader
def unauthorized_callback(error):
	return jsonify({
		"description" : "Unauthorised access - login is required",
		"error" : "unauthorised access"
	})

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	return decrypted_token['jti'] in BLACKLIST
 
@jwt.needs_fresh_token_loader
def fresh_token_callback():
	return jsonify({
		"description" : "Fresh access token is required - please login",
		"error" : "Login required"
	})

@jwt.revoked_token_loader
def revoked_token_callback():
	return jsonify({
		"description" : "User has logout of the api",
		"error" : "User logout"
	})


api.add_resource(User, "/user")
api.add_resource(UserRegistry, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Homepage, "/")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")


@app.before_first_request
def create_tables():
	db.create_all()






if __name__ == "__main__":
	db.init_app(app)
	app.run(port=5000, debug=True)

