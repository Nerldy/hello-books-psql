from flask import jsonify, abort
from ..models import BookList
from . import home


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

