from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .data import db
from .auth import login_manager
from .book.views import keeper
from .users.views import users

app = Flask(__name__)
app.config.from_object('config')


db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(keeper)
app.register_blueprint(users)