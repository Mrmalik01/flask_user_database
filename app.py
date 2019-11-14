from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from resources.user import User, UserRegistry, UserLogin
from database import db

app = Flask(__name__)

api = Api(app)

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "example"

class Homepage(Resource):
	@classmethod
	def get(self):
		return "<h1> Service working </h1>"

api.add_resource(User, "/user")
api.add_resource(UserRegistry, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Homepage, "/")



@app.before_first_request
def create_tables():
	db.create_all()






if __name__ == "__main__":
	db.init_app(app)
	app.run(port=5000, debug=True)

