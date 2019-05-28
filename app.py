import os 

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# allows to Flask expceptions raise their own exceptions
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'angel' # app.config['JWT_SECRET_KEY']
api = Api(app)

jwt = JWTManager(app) # not createing endpoit =  /auth

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
	if identity == 1: #Instead of hard-coding this, you should add a config file or a database
		return {'is_admin':True}

	return {'is_admin':False}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
	from database import db

	db.init_app(app)
	app.run(port=5000, debug=True)

