from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
	"""create a user"""

	__tabelename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(70), index=True, nullable=False, unique=True)
	username = db.Column(db.String(70), index=True, nullable=False, unique=True)
	password_hash = db.Column(db.String(140))
	is_admin = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		"""
		Prevent pasword from being accessed
		"""
		raise AttributeError('password is not a readable attribute.')

	@password.setter
	def password(self, password):
		"""
		Set password to a hashed password
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Check if hashed password matches actual password
		"""
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f'<Username: {self.username}>'


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Book(db.Model):
	__tablename__ = "books"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(160), nullable=False)
	isbn = db.Column(db.String(20), nullable=False, unique=True)

	def __repr__(self):
		return f'<Book: {self.title}>'
