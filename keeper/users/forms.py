from flask.ext.wtf import Form
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError

from .models import User

class LoginForm(Form):
	email = fields.StringField(validators=[InputRequired(), Email()])
	password = fields.StringField(validators=[InputRequired()])

	def validate_password(form, field):
		try:
			user = User.query.filter(User.email == form.email.data).one()
		except (MultipleResultsFound, NoResultFound):
			raise ValidationError("Username or Password does not match")
		if user is None:
			raise ValidationError("Username or Password does not match")
		if not user.is_valid_password(form.password.data):
			raise ValidationError("Username or Password does not match")

		form.user = user

class RegistrationForm(Form):
	name = fields.StringField("Username")
	email = fields.StringField(validators=[InputRequired(), Email()])
	password = fields.StringField(validators=[InputRequired()])

	def validate_email(form, field):
		user = User.query.filter(User.email == field.data).first()
		if user is not None:
			raise ValidationError("That username is not available.")
			