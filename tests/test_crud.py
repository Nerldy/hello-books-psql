import unittest
from flask_testing import TestCase

from app import create_app, db
from app.models import UserList, BorrowedBook, BookList, AuthorList
import os
from flask import abort


class TestBase(TestCase):

	def create_app(self):
		config_name = 'testing'
		app = create_app(config_name)
		app.config.update(
			SQLALCHEMY_DATABASE_URI='postgresql://user_tester:1234@localhost/test_hello_books_db'
		)
		return app

	def setUp(self):
		"""
		Will be called before every test
		"""

		db.create_all()

		# create test admin user
		test_admin = UserList(username="adminTest", password="admintest12345678", email='admintest', is_admin=True)

		# create test non-admin user
		test_user = UserList(username="test_user", password="testuser12345678", email='testuser@mail.com')

		# save users to database
		db.session.add(test_admin)
		db.session.add(test_user)
		db.session.commit()

	def tearDown(self):
		"""
		Will be called after every test
		"""

		db.session.remove()
		db.drop_all()


class TestModels(TestBase):

	def test_user_model(self):
		"""test number of users in the table"""
		self.assertEqual(UserList.query.count(), 2)

	def test_book_model(self):
		"""test number of books in the table"""

		# create dummy book
		dummy_book = BookList(
			title='hello books',
			isbn='1234567890',
			synopsis="The output above lets us know that our test setup is OK. Now let's write some tests."
		)

		# create dummy author
		dummy_author = AuthorList(
			first_name='john',
			last_name='doe'
		)

		dummy_book.authors.append(dummy_author)

		# save book to db
		db.session.add(dummy_book)
		db.session.add(dummy_author)
		db.session.commit()

		self.assertEqual(BookList.query.count(), 1)

	if __name__ == '__main__':
		unittest.main()
