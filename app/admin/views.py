from flask_login import current_user, login_required
from flask import abort, jsonify, request
from . import admin
from .. import db
from ..models import Book, Author
from cerberus import Validator
import re
import sys


def check_admin():
	"""
	Prevent non-admins from accessing the page
	:return: 403
	"""
	if not current_user.is_admin:
		abort(403)


# useful functions
def format_inputs(word):
	"""
	formats input string
	:param word:
	:return: string
	"""
	json_input = word.lower().strip()
	split_input = re.sub(' +', " ", json_input)
	return "".join(split_input)


# schemas
book_schema = {
	'title': {
		'type': 'string',
		'required': True,
		'empty': False
	},
	'isbn': {
		'type': "integer",
		'required': True
	},
	'synopsis': {
		'type': "string",
		'required': True,
		'minlength': 30,
		'maxlength': 300
	},
	'authors': {
		'type': 'list',
		'schema': {
			'type': 'dict',
			'schema': {
				'first_name': {
					'type': 'string',
					'minlength': 1
				},
				'middle_name': {
					'type': 'string',
					'nullable': True
				},
				'last_name': {
					'type': 'string',
					'minlength': 1
				}
			}
		}

	}

}
author_schema = {
	'first_name': {
		'type': "string",
		'required': True,
		"minlength": 1
	},
	'middle_name': {
		'type': "string",
		'required': True,
		'nullable': True
	},
	'last_name': {
		'type': 'string',
		'required': True,
		'minlength': 1
	}
}


@admin.route('/books')
@login_required
def api_admin_view_all_books():
	"""
	list all books
	create a book
	:return:
	"""

	check_admin()

	all_books = Book.query.all()
	view_books = []

	for book in all_books:  # loop through all the books and turn them into JSON
		book_author = []

		for author in book.authors:  # get book author(s) from the authors table
			author_details = {
				"id": author.id,
				"full_names": f"{author.first_name} {author.last_name}",
				"date_created": author.date_created,
				"date_modified": author.date_modified
			}

			if author.middle_name:
				# check if author has a middle name
				author_details['full_names'] += " " + author.middle_name

			book_author.append(author_details)  # add book author details

		obj = {
			"id": book.id,
			"title": book.title,
			'isbn': book.isbn,
			'synopsis': book.synopsis,
			'date_created': book.date_created,
			'date_modified': book.date_modified,
			'authors': book_author
		}
		view_books.append(obj)  # add book into the main list

	return jsonify({"books": view_books})


@admin.route('/books', methods=['POST'])
@login_required
def api_admin_create_book():
	"""
	create a book
	:return: 201
	"""

	check_admin()

	req_data = request.get_json()

	# Validate JSON data
	validate_book_schema = Validator(book_schema)
	if not req_data:
		abort(400)

	# check length of isbn
	isbn_str = str(req_data['isbn'])
	if (len(isbn_str) == 10) or (len(isbn_str) == 13):
		# validate book schema
		if validate_book_schema.validate(req_data) is not True:
			return jsonify({'errors': validate_book_schema.errors}), 400

		new_book = Book(
			title=format_inputs(req_data['title']),
			isbn=req_data['isbn'],
			synopsis=format_inputs(req_data['synopsis']).capitalize()
		)

		for author in req_data['authors']:
			first_name = format_inputs(author['first_name'])
			last_name = format_inputs(author['last_name'])
			middle_name = format_inputs(author['middle_name'])

			if not first_name:
				return jsonify({'error': "first_name cannot be empty"}), 400

			if not last_name:
				return jsonify({'error': "last_name cannot be empty"}), 400

			new_author = Author(first_name=first_name, last_name=last_name)

			if middle_name:
				new_author.middle_name = middle_name

			new_book.authors.append(new_author)
			db.session.add(new_author)
		try:
			db.session.add(new_book)
			db.session.commit()
		except:
			return jsonify({'error': f"something went wrong {sys.exc_info()[0]}"}), 400

		return jsonify({'created book': "success"}), 201

	return jsonify({'error': "isbn should be 10 or 13 digits long"}), 400
