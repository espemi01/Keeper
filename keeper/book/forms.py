from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.login import current_user
from .models import Group, Contact
from flask import Blueprint

class GroupForm(Form):
	name = fields.StringField(validators=[Required()])

class ContactForm(Form):
	# group = QuerySelectField(query_factory=Group.query.filter(g.user_id == user.id))

	name = fields.StringField(validators=[Required()])
	phone = fields.StringField(validators=[Required()])
	address = fields.TextField('', validators=[Required()])
	city = fields.TextField('', validators=[Required()])
	state = fields.TextField('', validators=[Required()])
	country = fields.TextField('', validators=[Required()])