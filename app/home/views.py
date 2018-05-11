from flask import jsonify, abort, request
from ..models import BookList
from . import home
from cerberus import Validator

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

validate_pagination_schema = Validator(pagination_schema)


@home.route('/api/v1/books/results')
def api_pagination():
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
				}

				book_results.append(book_obj)

			return jsonify({'current_page': book_pagination.page, 'all_pages': book_pagination.pages, 'books': book_results})

		except:
			return jsonify({"error": 'are all your queries integers? That or something else went wrong in your request'}), 400

	return jsonify({"error": validate_pagination_schema.errors}), 400


@home.route('/api/v1/books')
def api_get_all_books():
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


@home.route('/api/v1/books/<int:id>')
def api_get_book(id):
	book = BookList.query.filter(BookList.id == id).first()

	if book is None:
		abort(404)

	book_details = {
		'id': book.id,
		'title': book.title,
		'isbn': book.isbn,
		'synposis': book.synopsis
	}
	book_authors = []
	for author in book.authors:

		author_detail = {
			'first_name': author.first_name,
			'last_name': author.last_name
		}

		if author.middle_name:
			author_detail['middle_name'] = author.middle_name

		book_authors.append(author_detail)

	book_details['authors'] = book_authors

	return jsonify({"book": book_details})
