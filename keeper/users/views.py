from flask import Blueprint, Flask, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user

from .forms import LoginForm, RegistrationForm
from .models import User
from keeper.data import query_to_list

users = Blueprint('users', __name__)

@users.route("/")
def index():
	if not current_user.is_anonymous():
		return redirect(url_for("users.view_profile"))
	return render_template("index.html")

@users.route("/user")
@login_required
def view_profile(id=None):
	user = User.get_or_404(current_user.id)
	print(current_user.id)
	if not user.id == current_user.id:
		abort(401)
	query = user.query.filter(user.id == current_user.id)
	data = query_to_list(query)
	return render_template("users/view.html", info=data)

@users.route('/login/', methods=('GET', 'POST'))
def login():
	form = LoginForm()
	if form.validate_on_submit():
		login_user(form.user)
		flash("You were logged in!")
		return redirect(request.args.get("next") or url_for("keeper.index"))
	return render_template('users/login.html', form=form)

@users.route('/register/', methods=('GET', 'POST'))
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User.create(**form.data)
		login_user(user)
		return redirect(url_for('keeper.index'))
	return render_template('users/register.html', form=form)

@users.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('keeper.index'))