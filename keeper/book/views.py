from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask.ext.login import current_user, login_required

from .forms import GroupForm, ContactForm
from .models import Group, Contact
from keeper.data import query_to_list

keeper = Blueprint("keeper", __name__)qq
users = Blueprint("users", __name__)


@keeper.route("/groups/<name>")
@login_required
def view_group(name):
	group = Group.query.filter(Group.name == name)
	data = query_to_list(group)
	return render_template("book/view.html", info=data)

@keeper.route("/groups", methods=("GET", "POST"))
@login_required
def view_groups(group_id=None):
	groups = Group.get_or_404(current_user.id)
	
	query = Group.query.filter(Group.user_id == current_user.id)
	data = query_to_list(query)
	return render_template("book/view.html", info=data)

@keeper.route("/new", methods=("GET", "POST"))
@login_required
def new():
	form = ContactForm()
	groups = Group.query.filter(Group.user_id == current_user.id)

	if form.validate():
		Contact.create(**form.data)
		flash("Added New Contact")
		return redirect(url_for("users.index"))

	data = query_to_list(groups)
	return render_template("book/contact.html", groups=groups, data=data, user=current_user, form=form)

@keeper.route("/add_group", methods=("GET", "POST"))
@login_required
def add_group():
	form = GroupForm()

	if form.validate_on_submit():
		group = Group.create(owner=current_user, **form.data)
		flash("Added Group")
		return redirect(url_for('keeper.view_groups'))
	return render_template('book/group.html', form=form)

@keeper.route("/map", methods=("GET", "POST"))
@login_required
def view_map():
	form = ContactForm()

	if form.validate_on_submit():
		url=makeurl(form)
		return render_template('maps/googlemaps.html', url=url)
	return render_template('maps/mappage.html', form=form)

_LINK = Markup('<a href="{url}">{name}</a>')

def _group_link(group_id):
	url = url_for(".add_group", group_id=group_id)
	return _LINK.format(url=url, name=group_id)

def _con_link(contact_id):
	url = url_for(".")

def makeurl(form):
	address = str(request.form['address'])
	theaddress = address.replace(" ", "+")
	city = str(request.form['city'])
	thecity = city.replace(" ", "+")
	state = str(request.form['state'])
	thestate = state.replace(" ", "+")
	country = str(request.form['country'])
	thecountry = country.replace(" ", "+")
	thesource = "https://www.google.com/maps/embed/v1/place?q="+theaddress+",+"+thecity+",+"+thestate+",+"+thecountry+"&key=AIzaSyB3uDG5-6T0_AaVqwg10aoLab9sItnS7Iw"
	return thesource
