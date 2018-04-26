from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager, current_user, login_required
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
	login_manager.login_view = '/api/v1/auth/login'

	migrate = Migrate(app, db)

	from app import models

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/api/v1/admin')

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	return app
