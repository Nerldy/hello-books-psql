from flask import jsonify
from flask_login import login_required

from . import home


@home.route('/')
def homepage():
	return jsonify({"message": "Welcome to Hello Books"})


@home.route('/api/v1/books')
@login_required
def dashboard():
	return jsonify({"message": "logged in as admin"})
