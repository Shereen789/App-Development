import os
import datetime
from models import *
from create import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Flask, render_template, request
from flask import session
from flask_session import Session

# app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# Userdata.load(request.json, session=db.session)


@app.route("/batch/data")
def retrive():
    print(request.data)
    return request.data


@app.route("/")
def index():
    return "Project 1: TODO"


@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        return "Please Login using your Credentials"


@app.route("/search")
def search():
    return render_template('search.html')


@app.route("/sresults", methods=["POST"])
def sresults():

    search_by = request.form.get("search_with")
    search_text = "%"+request.form.get("search_text")+"%"
    print(search_by, search_text)
    if search_by == "1":
        results = db.query(Books).filter(
            Books.author.like(search_text)).all()
    if search_by == "2":
        results = db.query(Books).filter(
            Books.isbn.like(search_text)).all()
    if search_by == "3":
        results = db.query(Books).filter(
            Books.title.like(search_text)).all()
    if results != None:
        return render_template('searchresults.html', results=results)
    else:
        return "No such Details Found"


@app.route("/logout")
def logout():
    if "Email" in session:
        session.pop('Email', None)
        return render_template('logout.html')
    else:
        return "user already logged out"


@app.route("/home", methods=["POST"])
def home():
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        if not validate(uname, pwd):
            return "<h3>Incorrect UserId or Password</h3>"
            # return render_template('register.html')
        else:
            session['Email'] = request.form['Email']
            return render_template('success.html')


@app.route("/display", methods=["POST", "GET"])
def display():
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        if not validate(uname, pwd):
            tstamp = datetime.datetime.now()
            print(uname, pwd, tstamp)
            try:
                db.execute("INSERT INTO userdata(username, passwords, creationstamp) VALUES (:username, :passwords, :creationstamp)",
                           {"username": uname, "passwords": pwd, "creationstamp": tstamp})
                db.commit()
                return "Hello "+uname.split('@')[0]+"! You have successfully registered"
            except:
                return "Hello "+uname.split('@')[0] + "! Failed to Register"
        else:
            return "You are already registered."
    else:
        return "Please register yourself @ '/register'"


@app.route("/admin")
def admin():
    user_data = Userdata.query.all()
    return render_template('admin.html', userdata=user_data)


def validate(uname, pwd):
    checker = db.execute("SELECT username, passwords FROM userdata WHERE username = :id and passwords= :pwd",
                         {"id": uname, "pwd": pwd}).fetchone()
    if checker is None:
        return False
    else:
        return True
