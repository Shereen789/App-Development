import os
import datetime
from models import *
from create import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


@app.route("/")
def index():
    return "Project 1: TODO"


@app.route("/data/batch")
def codetime():
    print(request.data)
    return "Codetime Success!!"


@app.route("/register")
def register():
    return render_template('register.html')


# @app.route("/hello", methods=["POST"])
# def hello():
#     name = request.form.get("Email")
#     pwd = request.form.get("password")
#     print(name+"#"+pwd)
#     return "Hello "+name.split('@')[0]+"! You have successfully registered"


@app.route("/display", methods=["POST"])
def display():
    uname = request.form.get("Email")
    pwd = request.form.get("password")
    tstamp = datetime.datetime.now()
    print(uname, pwd, tstamp)
    try:
        db.execute("INSERT INTO userdata(username, passwords, creationstamp) VALUES (:username, :passwords, :creationstamp)",
                   {"username": uname, "passwords": pwd, "creationstamp": tstamp})
        db.commit()
        return "Hello "+uname.split('@')[0]+"! You have successfully registered"
    except:
        return "Hello "+uname.split('@')[0] + "! Failed to Register"


@app.route("/admin")
def admin():
    user_data = Userdata.query.all()
    lis = []
    for data in user_data:
        lis.append(data)
    return lis
