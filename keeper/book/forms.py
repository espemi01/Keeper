from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Group

class GroupForm(Form):
	name = fields.StringField(validators=[Required()])

class ContactForm(Form):
	name = fields.StringField(validators=[Required()], query_factory=lambda: Contact.query.all())
	phone = fields.StringField(validators=[Required()])
	address = fields.TextField('', validators=[Required()])
	city = fields.TextField('', validators=[Required()])
	state = fields.TextField('', validators=[Required()])
	country = fields.TextField('', validators=[Required()])