from keeper.data import CRUDMixin
from keeper import db
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class Group(CRUDMixin, db.Model):
	__tablename__ = 'groups'

	name = db.Column(db.String)
	contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __str__(self):
		return self.name

class Contact(CRUDMixin, db.Model):
	__tablename__ = 'contacts'

	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String)
	phone = db.Column(db.String)
	address = db.Column(db.String)
	city = db.Column(db.String)
	state = db.Column(db.String)
	country = db.Column(db.String)
	groups = db.relationship('Group', backref='contacts', lazy='dynamic')

	def __init__(self, id, name, phone, address, city, state, country, groups):
		self.id = id
		self.name = name
		self.phone = phone
		self.address = address
		self.city = city
		self.state = state
		self.country = country
		self.groups = groups

	def group(self, group):
		if not self.is_grouped(group):
			self.grouped.append(group)
			return self

	def ungroup(self, group):
		if self.is_grouped(group):
			self.grouped.remove(user)
			return self

	def is_grouped(self, group):
		return self.grouped.filter()

	def __repr__(self):
		return self.id