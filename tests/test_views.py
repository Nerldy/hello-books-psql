import unittest
from flask_testing import TestCase

from app import create_app, db
from app.models import UserList, BorrowedBook, BookList, AuthorList
import os
from flask import abort

def register_user(client, username, email, password):
	return client.post('/api/')

class TestBase(TestCase):

	def create_app(self):
		config_name = 'testing'
		app = create_app(config_name)
		app.config.update(
			SQLALCHEMY_DATABASE_URI='postgresql://localhost/test_hello_books_db'
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


class TestViews(TestBase):
	def test_home_view(self):
		res = self.client.get('/api/v1/books')
		self.assertIn('books', str(res.data))

	def test_login_view(self):
		res = self.client.post('/api/v1/auth/login')
		self.assertEqual(res.status_code, 401)

	def test_register_view(self):
		res = self.client.post('/api/v1/auth/register')
		self.assertEqual(res.status_code, 401)
