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
# from flask_cors import CORS, cross_origin


# cors = CORS(app, resources={r"*": {"origins": "*"}})
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
    return render_template('register.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        html = "{{url_for('register')}}"
        button = "Register"
        if uname == "" and pwd == "":
            return render_template('error.html', html=html, button=button, message="USERNAME AND PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if uname == "":
            return render_template('error.html', html=html, button=button, message="USERNAME CAN'T BE EMPTY. TRY AGAIN")
        if pwd == "":
            return render_template('error.html', html=html, button=button, message="PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if validate_user(uname):
            html = "{{url_for('login')}}"
            return render_template('error.html', html=html, button='Login', message="USER ALREADY EXISTS. LOGIN WITH THE CREDENTIALS")

        if uname != "" and pwd != "" and not validate_user(uname):
            try:
                tstamp = datetime.datetime.now()
                db.execute("INSERT INTO userdata(username, passwords, creationstamp) VALUES (:username, :passwords, :creationstamp)",
                           {"username": uname, "passwords": pwd, "creationstamp": tstamp})
                db.commit()
                return render_template('login.html')
            except:
                return render_template('error.html', html=html, button=button, message="Failed to Register. Try Again")
    else:
        return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        html = "{{url_for('login')}}"
        button = "Login"
        if uname == "" and pwd == "":
            return render_template('error.html', html=html, button=button, message="USERNAME AND PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if uname == "":
            return render_template('error.html', html=html, button=button, message="USERNAME CAN'T BE EMPTY. TRY AGAIN")
        if pwd == "":
            return render_template('error.html', html=html, button=button, message="PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if not validate_user(uname):
            html = "{{url_for('register')}}"
            return render_template('error.html', html=html, button='Register', message="USER DOESN'T EXISTS. REGISTER")
        elif not validate(uname, pwd):
            return render_template('error.html', html=html, button=button, message="PASSWORD NOT MATCHED. TRY AGAIN")

        session['Email'] = request.form['Email']
        return render_template('profile.html')

    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html')


@app.route("/search", methods=["POST"])
def search():
    search_by = request.form.get("search_with").strip()
    search_text = "%"+request.form.get("search_text").strip()+"%"
    print(search_by, search_text)
    if search_by == "1":
        results = db.query(Books).filter(Books.author.like(search_text)).all()
    if search_by == "2":
        results = db.query(Books).filter(Books.isbn.like(search_text)).all()
    if search_by == "3":
        results = db.query(Books).filter(Books.title.like(search_text)).all()
    if results != None:
        return render_template('search.html', results=results)
    else:
        return "No such Details Found"


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


def validate_user(uname):
    checker = db.execute("SELECT username, passwords FROM userdata WHERE username = :id",
                         {"id": uname}).fetchone()
    if checker is None:
        return False
    else:
        return True
