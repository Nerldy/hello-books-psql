from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile('config.py')
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	login_manager.init_app(app)
	login_manager.login_message = 'You must be logged in to access this page'
	login_manager.login_view = '/api/v1/auth/login'

	migrate = Migrate(app, db)

	from app import models

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/api/v1/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	from .users import users as users_blueprint
	app.register_blueprint(users_blueprint, url_prefix='/api/v1/users')

	@app.errorhandler(405)
	def method_not_allowed(error):
		return jsonify({"error": "method not allowed"}), 405

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({"error": "not found"}), 404

	@app.errorhandler(403)
	def method_not_allowed(error):
		return jsonify({"error": "forbidden"}), 403

	@app.errorhandler(400)
	def not_found(error):
		return jsonify({"error": "bad request"}), 400

	return app
