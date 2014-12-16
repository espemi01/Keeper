from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import Required
from flask.ext.login import current_user
from .models import Group, Contact

class GroupForm(Form):
	name = fields.StringField(validators=[Required()])

class ContactForm(Form):
	group_id = fields.StringField(validators=[Required()])
	name = fields.StringField(validators=[Required()])
	phone = fields.StringField(validators=[Required()])
	address = fields.TextField(validators=[Required()])
	city = fields.TextField(validators=[Required()])
	state = fields.TextField(validators=[Required()])
	country = fields.TextField(validators=[Required()])