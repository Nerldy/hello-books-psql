from flask_login import current_user, login_required
from flask import abort, jsonify
from . import admin
from .. import db
from ..models import Book, Author


def check_admin():
	"""
	Prevent non-admins from accessing the page
	:return: 403
	"""
	if not current_user.is_admin:
		abort(403)


@admin.route('/books')
@login_required
def api_admin_all_books():
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
				"first_name": author.first_name,
				"last_name": author.last_name
			}

			if author.middle_name:
				# check if author has a middle name
				author_details['middle_name'] = author.middle_name
			book_author.append(author_details)
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
