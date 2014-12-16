from keeper.data import CRUDMixin, db
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class Group(CRUDMixin, db.Model):
	__tablename__ = 'groups'

	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String)
	contacts = db.relationship('Contact', backref='group', lazy='select')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '<Group {:d} {}>'.format(self.id, self.name)

	def __str__(self):
		return self.name

class Contact(CRUDMixin, db.Model):
	__tablename__ = 'contacts'

	name = db.Column(db.String)
	phone = db.Column(db.String)
	address = db.Column(db.String)
	city = db.Column(db.String)
	state = db.Column(db.String)
	country = db.Column(db.String)
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))