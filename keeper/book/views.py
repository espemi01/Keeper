from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from .forms import GroupForm, ContactForm
from .models import Group, Contact
from keeper.data import query_to_list

keeper = Blueprint("keeper", __name__)

@keeper.route("/groups/<int:group_id>")
@login_required
def view_group(group_id=None):
	group = Group.get_or_404(group_id)
	if not group.user_id == current_user.id:
		abort(401)

	query = Contact.query.filter(Contact.group_id == group_id)
	data = query_to_list(query)
	return render_template("book/group.html", contacts=data, contact=contact)

@keeper.route("/groups", methods=("GET", "POST"))
@login_required
def view_groups(group_id=None):
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
	return render_template("book/view.html", info=results)

@keeper.route("/groups/<int:group_id>/new", methods=("GET", "POST"))
@login_required
def add_contact(group_id=None):
	group = Group.get_or_404(group_id)

	form = ContactForm(csrf_enabled=False)

	if form.validate():
		Contact.create(**form.data)
		return '', 204

	return jsonify(errors=form.errors), 400

# @keeper.route("/groups/<int:group_id>/<int:contact.id>")
# @login_required
# def view_map(group_id=None):


@keeper.route("/group", methods=("GET", "POST"))
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

@app.route("/map")
def index():
	gen_form = GenForm()
	return render_template("index.html",
							gen_form=gen_form)

@app.route("/mapshow", methods=("POST", ))
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

class GenForm(Form):
	address = fields.TextField('', validators=[validators.required()])
	city = fields.TextField('', validators=[validators.required()])
	state = fields.TextField('', validators=[validators.required()])
	country = fields.TextField('', validators=[validators.required()])

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
