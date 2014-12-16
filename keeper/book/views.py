from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from .forms import GroupForm, ContactForm
from .models import Group, Contact
from keeper.data import query_to_list

keeper = Blueprint("keeper", __name__)

@keeper.route("/groups/<name>")
@login_required
def view_group(id=None):
	group = Group.get_or_404(group_id)
	if not group.user_id == current_user.id:
		abort(401)

	query = Contact.query.filter(Contact.group_id == group_id)
	data = query_to_list(query)
	return render_template("book/group.html", contacts=data, contact=contact)

@keeper.route("/groups", methods=("GET", "POST"))
@login_required
def view_groups(group_id=None):
	group = Group.get_or_404(current_user.id)
	if not group.user_id == current_user.id:
		abort(401)
	query = user.query.filter(user.id == current_user.id)
	data = query_to_list(query)
	return render_template("book/view.html", info=data)

@keeper.route("/groups/<group>/new", methods=("GET", "POST"))
@login_required
def new(group):
	form = ContactForm(csrf_enabled=False)

	# if form.validate():
	# 	Contact.create(group=group, **form.data)
	# 	flash("Added New Contact")
	# 	return redirect(url_for("user.index"))

	# return jsonify(errors=form.errors), 400

@keeper.route("/add_group", methods=("GET", "POST"))
@login_required
def add_group():
	form = GroupForm()

	if form.validate_on_submit():
		Group.create(owner=current_user, **form.data)
		flash("Added Group")
		return redirect(url_for("user.index"))

	query = Group.query.filter(Group.user_id == current_user.id)
	data = query_to_list(query)
	results = []

	try:
		results = [next(data)]
		for row in data:
			row = [_make_link(cell) if i == 0 else cell for i, cell in enumerate(row)]
			results.append(row)
	except StopIteration:
		pass
	return render_template("book/group.html", group=results, form=form)

@keeper.route("/map")
@login_required
def view_map():
	gen_form = ContactForm()
	return render_template("mappage.html",
							gen_form=gen_form)

@keeper.route("/mapshow", methods=("POST", ))
def get_param():
	form = GenForm()
	if form.validate_on_submit():
		url=makeurl(form)
		return render_template('googlemaps.html', url=url)
	return render_template("error.html", form=form)

_LINK = Markup('<a href="{url}">{name}</a>')

def _make_link(group_id):
	url = url_for(".add_group", group_id=group_id)
	return _LINK.format(url=url, name=group_id)

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
