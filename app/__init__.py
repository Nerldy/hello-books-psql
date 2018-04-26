from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__, instance_relative_config=True)


def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	login_manager.init_app(app)
	login_manager.login_message = 'You must be logged in to access this page'
	login_manager.login_view = 'auth.login'

	migrate = Migrate(app, db)

	from app import models

	@app.route('/api/v1/books')
	def api_get_all_books():
		return jsonify({'message': "all books"})

	return app
