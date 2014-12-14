from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Group

class GroupForm(Form):
	name = fields.StringField(validators=[Required()])

class ContactForm(Form):
	name = fields.StringField(validators=[Required()], query_factory=lambda: Contact.query.all())
	address = fields.StringField(validators=[Required()])
	phone = fields.StringField(validators={Required()})