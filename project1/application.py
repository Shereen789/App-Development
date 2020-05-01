import os
import datetime
from models import *
from create import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Flask, render_template, request, redirect
from flask import session
from flask_session import Session
from flask import Flask, jsonify, json
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


@app.route("/", methods=["GET"])
def index():
    print("REACHED LOGIN")
    if request.method == "GET":
        if session.get("Email") is None:
            return render_template('login.html', message="")
        else:
            return render_template('profile.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        if uname == "" and pwd == "":
            return render_template('register.html', message="USERNAME AND PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if uname == "":
            return render_template('register.html', message="USERNAME CAN'T BE EMPTY. TRY AGAIN")
        if pwd == "":
            return render_template('register.html', message="PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if validate_user(uname):
            return render_template('login.html', message="USER ALREADY EXISTS. LOGIN WITH THE CREDENTIALS")

        if uname != "" and pwd != "" and not validate_user(uname):
            try:
                tstamp = datetime.datetime.now()
                db.execute("INSERT INTO userdata(username, passwords, creationstamp) VALUES (:username, :passwords, :creationstamp)",
                           {"username": uname, "passwords": pwd, "creationstamp": tstamp})
                db.commit()
                return render_template('login.html', message="Please Log In using your Credentials")
            except:
                return render_template('register.html', message="Failed to Register. Try Again")
    else:
        return render_template('register.html', message="Register Your self with Email and Password")


@app.route("/login", methods=["POST", "GET"])
def login():
    # session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        # if uname == "" and pwd == "":
        #     return render_template('login.html', message="USERNAME AND PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        # if uname == "":
        #     return render_template('login.html', message="USERNAME CAN'T BE EMPTY. TRY AGAIN")
        # if pwd == "":
        #     return render_template('login.html', message="PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        # if not validate_user(uname):
        #     return render_template('register.html', message="USER DOESN'T EXISTS. REGISTER")
        # elif not validate(uname, pwd):
        #     return render_template('login.html', message="PASSWORD NOT MATCHED. TRY AGAIN")

        session['Email'] = request.form['Email']
        return render_template('profile.html')

    else:
        return render_template('login.html')

        # return render_template('profile.html')


@app.route("/logout")
def logout():
    session.clear()
    return render_template('login.html', message="Please Log In using your Credentials")

# Basic search directing to new HTML PAGE
# @app.route("/search", methods=["POST"])
# def search():
#     if request.method == "POST":
#         search_by = request.form.get("search_with").strip()
#         search_text = "%"+request.form.get("search_text").strip()+"%"
#         print(search_by, search_text)
#         if search_by == "1":
#             results = db.query(Books).filter(
#                 Books.author.like(search_text)).all()
#         if search_by == "2":
#             results = db.query(Books).filter(
#                 Books.isbn.like(search_text)).all()
#         if search_by == "3":
#             results = db.query(Books).filter(
#                 Books.title.like(search_text)).all()
#         if results != None:
#             return render_template('search.html', results=results)
#         else:
#             return "No such Details Found"
# -----------------------------------------------------------------------------------
# WIth AJAX IMPLEMENTATION

# @app.route("/search", methods=["GET"])
# def search():
#     return render_template('profile.html')


@app.route("/api/search/<data>")
def search(data):
    print("I'm inside the search function along with ", data)
    # search_by = request.args.get("search_with")
    # search_text = request.args.get("search_text")
    search_by = data.split("&")[0]
    search_text = data.split("&")[1]
    print("data has been Splitted")
    search_list = []
    results = get_data(search_by, search_text)
    if results != None:
        for result in results:
            temp = {}
            isbn = result.isbn
            title = result.title
            author = result.author
            temp["isbn"] = isbn
            temp["title"] = title
            temp["author"] = author
            search_list.append(temp)
        print("====================================")
        print(type(json.dumps(search_list)))
        print(json.dumps(search_list))
        jsonStr = json.dumps(search_list)
        return jsonify(jsonStr)
    else:
        return (jsonify({"Error": "No such Details Found"}), 400)


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


def get_data(i, text):
    results = []
    text = "%"+text+"%"
    if i == "1":
        results = db.query(Books).filter(
            Books.author.like(text)).all()
    if i == "2":
        results = db.query(Books).filter(
            Books.isbn.like(text)).all()

    if i == "3":
        results = db.query(Books).filter(
            Books.title.like(text)).all()
    return results
