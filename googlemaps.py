from flask import flash, Flask, Markup, redirect, render_template, url_for, request
from flask.ext.wtf import Form
from wtforms import fields, validators
import random

SECRET_KEY = 'some-key-that-should-work'
WTF_CSRF_SECRET_KEY = 'some-key-that-also-should-work'


app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

class GenForm(Form):
	address = fields.TextField('', validators=[validators.required()])
	city = fields.TextField('', validators=[validators.required()])
	state = fields.TextField('', validators=[validators.required()])
	country = fields.TextField('', validators=[validators.required()])
    
    
@app.route("/")
def index():
	gen_form = GenForm()
	return render_template("mappage.html",
							gen_form=gen_form)

@app.route("/map", methods=("POST", ))
def get_param():
	form = GenForm()
	if form.validate_on_submit():
		url=makeurl(form)
		return render_template('googlemaps.html', url=url)
	return render_template("error.html", form=form)
	
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





if __name__ == '__main__':
    app.run()



