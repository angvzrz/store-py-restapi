from app import app
from database import db

@app.before_first_request
def create_tables():
	db.create_all()

db.init_app(app)