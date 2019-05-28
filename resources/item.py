from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help="This field cannot be left blank!"		
	)

	parser.add_argument(
		'store_id',
		type=int,
		required=True,
		help="Every item needs a store id"		
	)

	@jwt_required
	def get(self, name):
		try:
			item = ItemModel.find_by_name(name)	
		except:
			return {'message':'An error occured doing the search.'}	

		if item:
			return item.json()

		return {'message':'Item not found'}, 404

	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message':"An item with the name '{}' already exists".format(name)}, 400

		data = Item.parser.parse_args()
		item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:
			return {'message':'An error occured inserting the item.'}, 500 #500 = Internal Server Error	

		return item.json(), 201

	#@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			try:		
				item = ItemModel(name, **data)
			except:
				return {'message':'An error occured inserting the item.'}, 500
		else:
			try:
				item.price = data['price']
			except:
				return {'message':'An error occured updating the item.'}, 500	

		item.save_to_db()

		return item.json()

	@jwt_required
	def delete (self, name):
		claims = get_jwt_claims()

		if not claims['is_admin']:
			return {'message':'Admin privilige required'}, 401

		item = ItemModel.find_by_name(name)

		if item:
			item.delete_from_db()
		
		return {'message':'Item deleted'}


class ItemList(Resource):
	def get(self):
		return {'items':[item.json() for item in ItemModel.find_all()]}
		#return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}