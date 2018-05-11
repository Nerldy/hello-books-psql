from flask_login import current_user, login_required
from flask import abort, jsonify, request
from . import admin
from .. import db
from ..models import BookList, AuthorList, BorrowedBook, UserList
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
		'type': "string",
		'required': True
	},
	'synopsis': {
		'type': "string",
		'required': True,
		'minlength': 30,
		'maxlength': 1000
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

update_book_schema = {
	'title': {
		'type': 'string',
		'empty': False
	},
	'synopsis': {
		'type': "string",
		'minlength': 30,
		'maxlength': 350
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

pagination_schema = {
	'limit': {
		'type': 'string',
		'required': True
	},
	'page_num': {
		'type': 'string',
		'required': True
	}
}

book_schema_validate = Validator(book_schema)
author_schema_validate = Validator(author_schema)
update_book_schema_validate = Validator(update_book_schema)
validate_pagination_schema = Validator(pagination_schema)


@admin.route('/books/results')
@login_required
def api_admin_pagination():
	check_admin()

	req_args = request.args

	if validate_pagination_schema.validate(req_args):
		try:
			page_limit_json = int(request.args.get('limit', None))  # check if page limit is provided
			page_number = int(request.args.get('page_num', None))
			book_pagination = BookList.query.paginate(per_page=int(page_limit_json), page=page_number, error_out=True)
			book_results = []

			for book in book_pagination.items:
				book_obj = {
					'id': book.id,
					'title': book.title,
					'isbn': book.isbn,
					'synopsis': book.synopsis,
					'date_created': book.date_created,
					'date_modified': book.date_modified
				}

				book_results.append(book_obj)

			return jsonify({'current_page': book_pagination.page, 'all_pages': book_pagination.pages, 'books': book_results})

		except:
			return jsonify({"error": 'are all your queries integers? That or something else went wrong in your request'}), 400

	return jsonify({"error": validate_pagination_schema.errors}), 400


@admin.route('/books')
@login_required
def api_admin_view_all_books():
	"""
	list all books
	create a book
	:return:
	"""

	check_admin()

	all_books = BookList.query.all()
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
		duplicate_book = BookList.query.filter(BookList.isbn == req_data['isbn']).first()

		if duplicate_book is None:

			str_isbn = str(req_data['isbn'])

			if ((len(str_isbn) == 10) or (len(str_isbn) == 13)) and (str_isbn.isnumeric()):

				new_book = BookList(
					title=format_inputs(req_data['title']),
					isbn=req_data['isbn'],
					synopsis=format_inputs(req_data['synopsis'])
				)

				for author in req_data['authors']:
					first_name = format_inputs(author['first_name'])
					last_name = format_inputs(author['last_name'])
					new_author = AuthorList(first_name=first_name, last_name=last_name)
					middle_name = format_inputs(author['middle_name'])

					if middle_name:
						new_author.middle_name = middle_name

					new_book.authors.append(new_author)
					db.session.add(new_author)

				try:
					db.session.add(new_book)
					db.session.commit()
					return jsonify({'message': "BookList created"}), 201
				except:
					return jsonify({'error': "something went wrong"}), 400

			return jsonify({'error': "isbn length must be 10 or 13 digits and must only contain numbers"}), 400

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
		book = BookList.query.filter(BookList.id == id).first()

		if book is None:
			abort(404)

		if 'title' in req_data:
			title = format_inputs(req_data['title'])
			if len(title) < 1:
				return jsonify({'error': "title cannot be empty"})
			book.title = title

		if 'synopsis' in req_data:
			synopsis = format_inputs(req_data['synopsis'])
			if len(synopsis) < 1:
				return jsonify({'error': "synopsis cannot be empty"})
			book.synopsis = synopsis

		db.session.commit()

		return jsonify({"message": f"BookList with ID {id} has been updated"})

	return jsonify({"message": update_book_schema_validate.errors}), 400


@admin.route('/books/<int:id>', methods=['DELETE'])
@login_required
def api_delete_book(id):
	"""
	delete a book
	:param id: id
	:return: 201, 404
	"""
	delete_book = BookList.query.filter(BookList.id == id).first()

	if delete_book is None:
		abort(404)

	db.session.delete(delete_book)
	db.session.commit()

	return jsonify({"message": "book deleted"})


@admin.route('/books/<int:user_id>')
@login_required
def api_admin_find_user_who_has_not_returned_book(user_id):
	"""
	find all books not yet returned by user
	:param user_id:
	:return: books not returned, 404
	"""

	check_admin()

	user_borrowed_books = BorrowedBook.query.filter(BorrowedBook.user_id == user_id).all()
	books_borrowed = BookList.query.filter(BookList.is_borrowed == True).all()

	books_not_returned = []
	for book in books_borrowed:
		for user_book in user_borrowed_books:
			if book.id == user_book.book_id and user_book.return_date == None:
				book_obj = {
					'id': book.id,
					'title': book.title,
					'date_borrowed': user_book.borrow_date
				}
				books_not_returned.append(book_obj)

	return jsonify({f'books not returned by user {user_id}': books_not_returned})


@admin.route('/books/user/history/<int:user_id>')
@login_required
def api_user_history(user_id):
	"""
	:param user_id:
	:return: uhistory of books user borrowed and returned
	"""
	check_admin()

	req_args = request.args

	# enter this block if args are provided
	if validate_pagination_schema.validate(req_args):
		# confirm if user exists
		user_exist = UserList.query.filter(UserList.id == user_id).first()

		if user_exist is None:
			abort(404)

		try:
			# find user borrowed books that have been returned
			page_limit = int(req_args.get('limit', None))
			page_num = int(req_args.get('page_num', None))
			user_borrowed_books = BorrowedBook.query.filter(BorrowedBook.user_id == user_id). \
				filter(BorrowedBook.return_date != None). \
				paginate(per_page=int(page_limit), page=page_num, error_out=True)

			# empty history book list holder
			books_history_list = []

			# create book history list
			for book_id in user_borrowed_books.items:
				all_books = BookList.query.filter(BookList.id == book_id.book_id).first()

				book_obj = {
					'id': all_books.id,
					'title': all_books.title,
					'date_borrowed': book_id.borrow_date,
					'date_returned': book_id.return_date
				}

				books_history_list.append(book_obj)
			return jsonify({
				"user_details": {
					'username': user_exist.username,
					'user_id': user_id,
					'email': user_exist.email
				},
				'borrowed_book_history': {
					'books': books_history_list
				},
				'page_details': {
					'current_page': user_borrowed_books.page,
					'all_pages': user_borrowed_books.pages,
					'total_results': user_borrowed_books.total
				}
			})
		except:
			return jsonify({"error": 'are all your queries integers? That or something else went wrong in your request'}), 400

	return jsonify({'error': validate_pagination_schema.errors})
