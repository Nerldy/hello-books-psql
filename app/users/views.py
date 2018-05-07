from flask_login import login_required, current_user
from flask import jsonify, abort
from . import users
from .. import db
from ..models import BookList, BorrowedBook


@users.route('/books/<int:id>', methods=['POST'])
@login_required
def api_users_borrow_book(id):
	# find book id
	book = BookList.query.filter(BookList.id == id).first()
	user_id = current_user.get_id()
	borrow_book = BorrowedBook()

	# if book exists:
	if not book:
		abort(404)

	# if book.user_id == user_id:
	# 	return jsonify({'message': "you currently have this book borrowed"})

	if book.is_borrowed:
		return jsonify({'message': f"BookList with ID {book.id} is not currently available."})

	borrow_book.user_id = user_id
	borrow_book.book_id = book.id
	book.is_borrowed = True

	db.session.add(borrow_book)

	db.session.commit()
	# add it to the borrowing table
	return jsonify({"book_borrowed": f"{book.title}"})


@users.route('/books/<int:id>', methods=['PUT'])
@login_required
def api_return_book(id):
	book = BookList.query.filter(BookList.id == id).first()
	user_id = current_user.get_id()

	# if book exists:
	if not book:
		abort(404)

	if book.user_id == user_id:
		book.is_borrowed = False
		db.session.delete(book)


@users.route('/books/<int:id>', methods=['PUT'])
@login_required
def api_get_users_borrowed_book(id):
	user_id = current_user.get_id()
	book = book = BookList.query.filter((BookList.id == id) and (BookList.user_id == user_id)).first()

	if not book:
		abort(404)

	return jsonify({'message': f"{book.title}"})
