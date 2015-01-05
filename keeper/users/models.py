from random import SystemRandom
import random

from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from keeper.data import CRUDMixin
from keeper import db

class User(UserMixin, CRUDMixin, db.Model):
	__tablename__ = 'users'

	name = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(120))
	_password = db.Column(db.LargeBinary(120))
	_salt = db.Column(db.String(120))
	groups = db.relationship('Group', backref='owner', lazy='dynamic')

	def __init__(self, name, email, _password, _salt, groups):
		self.name = name
		self.name = email
		self._password = _password
		self.groups = groups

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def password(self, value):
		if self._salt is None:
			self._salt = bytes(SystemRandom().getrandbits(1))
		self._password = self._hash_password(value)

	def is_valid_password(self, password):
		new_hash = self._hash_password(password)
		return compare_digest(new_hash, self._password)

	def _hash_password(self, password):
		p = password.encode("utf-8")
		salt = bytes(self._salt)
		buff = pbkdf2_hmac("sha512", p, salt, iterations=100000)
		return bytes(buff)

	def __repr__(self):
		return "<User #{:d}>".format(self.id)
		