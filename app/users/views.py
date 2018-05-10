from flask_login import login_required, current_user
from flask import jsonify, abort, request
from . import users
from .. import db
from ..models import BookList, BorrowedBook


@users.route('/books/<int:id>', methods=['POST'])
@login_required
def api_users_borrow_book(id):
	book = BookList.query.filter(BookList.id == id).first()  # find book with same id in the books list table
	user_id = current_user.get_id()  # current user id
	borrow_book = BorrowedBook()  # instance borrow book class

	# if book exists:
	if not book:
		abort(404)

	if book.is_borrowed:  # check if book is borrowed
		return jsonify({'message': f"BookList with ID {book.id} is not currently available."})

	borrow_book.user_id = user_id  # create a user id property
	borrow_book.book_id = book.id  # create a book id property
	book.is_borrowed = True  # make book borrow property status true

	# add it to the borrowing table
	db.session.add(borrow_book)
	db.session.commit()
	return jsonify({"book_borrowed": f"{book.title}"})


@users.route('/books/<int:id>', methods=['PUT'])
@login_required
def api_return_book(id):
	book = BorrowedBook.query.filter(BorrowedBook.book_id == id).first()  # find the book in the borrow table
	main_book = BookList.query.filter(BookList.id == id).first()  # find the sam book id in the books list table
	user_id = current_user.get_id()  # current user id

	# if book exists:
	if not book:
		abort(404)

	if main_book.is_borrowed:  # check if book is borrowed
		main_book.is_borrowed = False  # make it false
		book.return_date = db.func.current_timestamp()  # add current time stamp of when book is being return
		db.session.commit()

		return jsonify({"message": f'book with ID {book.book_id} has been returned'})

	abort(400)


@users.route('/books')
@login_required
def api_books_not_returned():
	req_data = request.args.get('returned', None)  # confirm if returned property exists in arguments

	# find user id in the borrow books table and confirm if it match current user
	user_borrowed_books = BorrowedBook.query.filter(BorrowedBook.user_id == current_user.get_id())

	if req_data:  # enter this block if returned property does exist in arguments
		books_not_returned = []  # empty books returned list
		book = BookList.query.all()  # get all books in the book list table

		if req_data.lower() == 'false':  # make the value of the returned proprty into small caps

			for book_borrowed in book:  # loop through the books list
				if book_borrowed.is_borrowed:  # check status of the book if it's borrowed
					book_obj = { # create the book object
						'id': book_borrowed.id,
						'title': book_borrowed.title,
						'isbn': book_borrowed.isbn,
						'synopsis': book_borrowed.synopsis,
						'date_borrowed': book_borrowed.borrow_date
					}

					books_not_returned.append(book_obj) # add book object to the not returned list

			return jsonify({'books yet to be returned': books_not_returned})
		abort(404)

	if user_borrowed_books is not None:
		all_borrowed_books = []

		for book_borrowed in user_borrowed_books:
			book = BookList.query.filter(BookList.id == book_borrowed.book_id).first()

			if book.is_borrowed is False:
				book_obj = {
					'title': book.title,
					'date_borrowed': book_borrowed.borrow_date,
					'date_returned': book_borrowed.return_date
				}

				all_borrowed_books.append(book_obj)

		return jsonify({'history_of_books_borrowed': all_borrowed_books})

# if req_data:
# 	all_books = []
# 	if req_data.lower() == 'false':
#
# 		for b in user_borrowed_books:
# 			for e in books_not_returned:
# 				if e.book_id == b.id:
# 					make_book = {
# 						'book_id': b.id,
# 						'title': b.title,
# 						'isbn': b.isbn,
# 						'synopsis': b.synopsis,
# 						'date_borrowed': e.borrow_date
# 					}
# 					all_books.append(make_book)
# 		return jsonify({"Books not yet returned": all_books})
#
# 	abort(404)

# if user_borrowed_books is not None:
# 	all_books = []
# 	for book_borrowed in available_books:
# 		for e in books_returned:
# 			if e.id == book_borrowed.id:
# 				make_book = {
# 					'book_id': book_borrowed.id,
# 					'title': book_borrowed.title,
# 					'isbn': book_borrowed.isbn,
# 					'synopsis': book_borrowed.synopsis,
# 					'date_borrowed': e.borrow_date,
# 					'date_returned': e.return_date
# 				}
# 				all_books.append(make_book)
# 	return jsonify({"history of borrowed books": all_books})
