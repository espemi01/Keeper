from flask import abort, Blueprint, flash, jsonify, Markup, redirect, render_template, request, url_for
from flask.ext.login import current_user, login_required

from .forms import GroupForm, ContactForm
from .models import Group, Contact
from keeper.data import query_to_list

keeper = Blueprint("keeper", __name__)

@keeper.route("/groups/<int:group_id>")
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

@keeper.route("/user/<group>/new", methods=("GET", "POST"))
@login_required
def new(group):
	g = Group.get_or_404(group)

	form = ContactForm(csrf_enabled=False)

	if form.validate():
		Contact.create(**form.data)
		return '', 204

	return jsonify(errors=form.errors), 400

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

_LINK = Markup('<a href="{url}">{name}</a>')

def _make_link(group_id):
	url = url_for(".add_group", group_id=group_id)
	return _LINK.format(url=url, name=group_id)
