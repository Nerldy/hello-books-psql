from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import arrow
from app import db, login_manager

utc = arrow.utcnow()  # create time object


# class UserLibraryList(db.Model):
# 	__tablename__ = 'user_library_list'
# 	id = db.Column(db.Integer, primary_key=True)
# 	date_borrowed = db.Column(db.DateTime, default=db.func.current_timestamp())
#
# 	# relationships
# 	users = db.relationship('UserList', backref='library', lazy='dynamic')


class UserList(UserMixin, db.Model):
	"""create a user"""

	__tablename__ = 'user_list'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(70), index=True, nullable=False, unique=True)
	username = db.Column(db.String(70), index=True, nullable=False, unique=True)
	password_hash = db.Column(db.String(140), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	is_logged = db.Column(db.Boolean, default=False)
	join_date = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	# relationships
	# library_id = db.Column(db.Integer, db.ForeignKey('user_library_list.id'))
	borrowed_books = db.relationship('BorrowedBook', backref='user_list', lazy='dynamic')

	@property
	def password(self):
		"""
		Prevent password from being accessed
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
	return UserList.query.get(int(user_id))


class BookList(db.Model):
	"""represents a book"""
	__tablename__ = "book_list"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(160), nullable=False)
	isbn = db.Column(db.String(13), nullable=False, unique=True)
	synopsis = db.Column(db.String(350), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	is_borrowed = db.Column(db.Boolean, default=False)

	authors = db.relationship('AuthorList', secondary="books_authors", backref='book_list', lazy='dynamic')
	borrowed_books = db.relationship('BorrowedBook', backref='book_list', lazy='dynamic')

	def __repr__(self):
		return f'<Book: {self.title}>'


class AuthorList(db.Model):
	"""represents the authors"""

	__tablename__ = 'author_list'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30), nullable=False)
	middle_name = db.Column(db.String(30), nullable=True)
	last_name = db.Column(db.String(30), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	def __repr__(self):
		return f"<Author: {self.first_name} {self.last_name}>"


class BorrowedBook(db.Model):
	__tablename__ = 'borrowed_books'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user_list.id'))
	book_id = db.Column(db.Integer, db.ForeignKey('book_list.id'))


# class BorrowedBookHistoryList(db.Model):
# 	__tablename__ = 'borrow_history'
# 	id = db.Column(db.Integer, primary_key=True)
# 	library_user_id = db.Column(db.Integer, db.ForeignKey('library_user_list.id'))
# 	book_id = db.Column(db.Integer, db.ForeignKey('book_list.id'))
# 	date_returned = db.Column(db.DateTime, default=db.func.current_timestamp())


db.Table(
	'books_authors',
	db.Column('book_id', db.Integer, db.ForeignKey('book_list.id')),
	db.Column('author_id', db.Integer, db.ForeignKey('author_list.id'))
)
