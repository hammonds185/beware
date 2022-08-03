from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy
from flask_session import Session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = "static/uploads"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
proxied = FlaskBehindProxy(app)
session = Session(app)
