from ..models import User
from .. import db
from . import auth
from flask_login import login_required, login_user, logout_user
from flask import request, jsonify, redirect, url_for, abort
import re


# useful functions
def format_inputs(word):
	"""
	formats input string
	:param word:
	:return: string
	"""
	json_input = word.title().strip()
	split_input = re.sub(' +', " ", json_input)
	return "".join(split_input)


@auth.errorhandler(401)
def error_401(e):
	return jsonify({"error": "Something went wrong"}), 401


@auth.route('/api/v1/auth/register', methods=['POST'])
def api_register():
	"""
	register user
	:return: 201,401
	"""

	if not request.json:
		abort(401)

	if 'username' not in request.json:
		abort(401)
	if 'password' not in request.json:
		abort(401)

	if 'username' in request.json:
		username = format_inputs(request.json['username'])

		if len(username) < 1:
			return jsonify({"error": "username field cannot be empty"}), 401
		else:
			request.json['username'] = username.lower()

	if 'password' in request.json:
		request.json['password'] = request.json['password'].strip()
		split_password = request.json['password'].split(" ")
		join_password = "".join(split_password)

		if len(join_password) != len(request.json['password']):
			return jsonify({"error": "password cannot have space characters in it"}), 401

		if len(request.json['password']) < 8 or request.json['password'] == "":
			return jsonify({"error": "password must be 8 characters or more"}), 401

	req_data = request.get_json()
	user = User()
	user.username = req_data.get('username', None)
	user.email = req_data.get('email', None)
	user.password = req_data.get('password', None)

	db.session.add(user)
	db.session.commit()

	return jsonify({"success": "You registered"}), 201


@auth.route('/api/v1/auth/login', methods=['POST'])
def api_login():
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		abort(401)

	if 'password' not in request.json:
		abort(401)

	if 'email' not in request.json:
		abort(401)

	user = User.query.filter_by(username=request.json['username']).first()

	if user is not None and user.verify_password(request.json['password']):
		login_user(user)

		return jsonify({"message": f"logged in {request.json['username']}"})

	return jsonify({"error": "email, password or username is invalid"}), 401


@auth.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def api_logout():
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		abort(401)

	if 'password' not in request.json:
		abort(401)

	if 'email' not in request.json:
		abort(401)

	user = User.query.filter_by(username=request.json['username']).first()

	if user is not None and user.verify_password(request.json['password']):
		logout_user()

		return jsonify({'message': "succesfully logged out"})

	return jsonify({"message": "you aren't logged in"}), 401
