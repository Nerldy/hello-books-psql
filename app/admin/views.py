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
		'required': True,
		'schema': {
			'type': 'dict',
			'schema': {
				'first_name': {
					'type': 'string',
					'required': True,
					'minlength': 1
				},
				'middle_name': {
					'type': 'string',
					'required': True,
					'nullable': True
				},
				'last_name': {
					'type': 'string',
					'required': True,
					'minlength': 1
				}
			}
		}

	}

}

updat_book_schema = {
	'title': {
		'type': 'string',
		'empty': False
	},
	'synopsis': {
		'type': "string",
		'minlength': 30,
		'maxlength': 300
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

book_schema_validate = Validator(book_schema)
author_schema_validate = Validator(author_schema)
update_book_schema_validate = Validator(updat_book_schema)


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

	if not req_data:
		abort(400)

	# validate json schema
	if book_schema_validate.validate(req_data):
		# check if book exists
		duplicate_book = Book.query.filter(Book.isbn == req_data['isbn']).first()

		if duplicate_book is None:

			str_isbn = str(req_data['isbn'])

			if (len(str_isbn) == 10) or (len(str_isbn) == 13):

				new_book = Book(
					title=format_inputs(req_data['title']),
					isbn=int(req_data['isbn']),
					synopsis=format_inputs(req_data['synopsis'])
				)

				for author in req_data['authors']:
					new_author = Author(first_name=format_inputs(author['first_name']), last_name=format_inputs(author['last_name']))
					middle_name = format_inputs(author['middle_name'])

					if middle_name:
						new_author.middle_name = middle_name

					new_book.authors.append(new_author)
					db.session.add(new_author)

				try:
					db.session.add(new_book)
					db.session.commit()
					return jsonify({'message': "Book created"}), 201
				except:
					raise
					return jsonify({'error': "something went wrong"}), 400

			return jsonify({'error': "isbn length must be 10 or 13 digits"}), 400

		return jsonify({'error': f"book with ISBN {req_data['isbn']} already exists."}), 400

	return jsonify({"error": book_schema_validate.errors}), 400


@admin.route('/books/<int:id>', methods=['PUT'])
@login_required
def api_update_book(id):
	"""
	update the book
	:return:
	"""

	check_admin()

	if update_book_schema_validate.validate(request.get_json()):
		req_data = request.get_json()
		new_book_data = {
			'title': req_data['title'],
			'synopsis': req_data['synopsis']
		}
		book = db.session.query(Book).filter(Book.id == id).update(new_book_data)
		db.session.commit()

		return jsonify({"message": f"Book with ID {id} has been updated"})

	return jsonify ({"message": book_schema_validate.errors})
