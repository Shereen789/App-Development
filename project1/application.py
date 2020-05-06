import os
import datetime
from models import *
from create import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Flask, render_template, request, redirect, jsonify
from flask import session
from flask_session import Session
#app = Flask(__name__)


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
    return render_template('register.html', message="Register Your self with Email and Password")


@app.route("/register", methods=["POST", "GET"])
def register():
    session.clear()
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        return "Please Login using your Credentials"


@app.route("/logout")
def logout():
    if "Email" in session:
        session.pop('Email', None)
        return render_template('logout.html')
    else:
        return "user already logged out"


@app.route("/home", methods=["POST"])
def home():

    session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        # html = "{{url_for('register')}}"
        # button = "Register"
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
    session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        # html = "{{url_for('register')}}"
        # button = "Register"
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



# @app.route("/display", methods=["POST", "GET"])
# def display():
#     if request.method == "POST":
#         uname = request.form.get("Email")
#         pwd = request.form.get("password")
#         if not validate(uname, pwd):
#             tstamp = datetime.datetime.now()
#             print(uname, pwd, tstamp)
#             try:
#                 db.execute("INSERT INTO userdata(username, passwords, creationstamp) VALUES (:username, :passwords, :creationstamp)",
#                            {"username": uname, "passwords": pwd, "creationstamp": tstamp})
#                 db.commit()
#                 return "Hello "+uname.split('@')[0]+"! You have successfully registered"
#             except:
#                 return "Hello "+uname.split('@')[0] + "! Failed to Register"
#         else:
#             return "You are already registered."
# =======
#         # html = "{{url_for('login')}}"
#         # button = "Login"
#         if uname == "" and pwd == "":
#             return render_template('login.html', message="USERNAME AND PASSWORD CAN'T BE EMPTY. TRY AGAIN")
#         if uname == "":
#             return render_template('login.html', message="USERNAME CAN'T BE EMPTY. TRY AGAIN")
#         if pwd == "":
    #         return render_template('login.html', message="PASSWORD CAN'T BE EMPTY. TRY AGAIN")
    #     if not validate_user(uname):
    #         return render_template('register.html', message="USER DOESN'T EXISTS. REGISTER")
    #     elif not validate(uname, pwd):
    #         return render_template('login.html', message="PASSWORD NOT MATCHED. TRY AGAIN")

    #     session['Email'] = request.form['Email']
    #     return render_template('profile.html')

    # else:
    #     return render_template('login.html', message="Please Login with your Credentials")


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
        return render_template('search.html', results=results
    else:
        return "No such Details Found"



@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        uname = request.form.get("Email")
        pwd = request.form.get("password")
        # html = "{{url_for('login')}}"
        # button = "Login"
        if uname == "" and pwd == "":
            return render_template('login.html', message="USERNAME AND PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if uname == "":
            return render_template('login.html', message="USERNAME CAN'T BE EMPTY. TRY AGAIN")
        if pwd == "":
            return render_template('login.html', message="PASSWORD CAN'T BE EMPTY. TRY AGAIN")
        if not validate_user(uname):
            return render_template('register.html', message="USER DOESN'T EXISTS. REGISTER")
        elif not validate(uname, pwd):
            return render_template('login.html', message="PASSWORD NOT MATCHED. TRY AGAIN")

        session['Email'] = request.form['Email']
        return render_template('profile.html')

    else:
        return render_template('login.html', message="Please Login with your Credentials")


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

@app.route("/bookpage/<string:arg>", methods = ["POST", "GET"])
def bookpage(arg):
    isbn = arg.strip().split("=")[1]
    if request.method == "GET":
        if not 'Email' in session:
            return render_template("register.html")
        #isbn = "1416949658"
        #isbn = "0553803700"
        book = Books.query.get(isbn)
        if book is None:
            return render_template("profile.html", msg = "Invalid ISBN number")
        reviews = Reviews.query.filter_by(isbn = isbn).all()
        return render_template("bookpage.html", bookDetails = book, userreviews = reviews)
    else:
        #isbn = "1416949658"
        #isbn = "0553803700"
        book = Books.query.get(isbn)
        try:
            rating = request.form["rate"]
        except:
            rating = 0
        review = request.form["feedback"]
        username = session['Email']
        
        #newReview = Reviews(username = username, isbn = isbn, rating = rating, review = review)
        dupReview = Reviews.query.filter(and_(Reviews.username == username, Reviews.isbn == isbn)).all()
        if not dupReview:
            db.execute("INSERT INTO reviewsdata(username, isbn, rating, review) VALUES (:username, :isbn, :rating, :review)",
                           {"username": username, "isbn": isbn, "rating": rating, "review": review})
            db.commit()
            #db.session.add(newReview)
            #db.session.commit()
            reviews = Reviews.query.filter_by(isbn = isbn).all()
            return render_template("bookpage.html", bookDetails = book, userreviews = reviews)
        else:
            reviews = Reviews.query.filter_by(isbn = isbn).all()
            return render_template("bookpage.html", bookDetails = book, userreviews = reviews, err_msg = "Duplicate")

@app.route("/api/book/<string:arg>", methods = ["GET"])
def api_bookpage(isbn):
    isbn = arg.strip().split("=")[1]
    book = Book.query.get(isbn)
    if book is None:
        result = {
            "status": 404,
            "error": "Book not found"
        }
        return jsonify(result)
    else:
        reviews = Review.query.filter_by(isbn = isbn).all()
        reviewDetails = []
        for r in reviews:
            newReview = {
                'username': r.username,
                'isbn': r.isbn,
                'rating':r.rating,
                'review':r.review,
            }
            reviewDetails.append(newReview)
        result = {
            "status": 200,
            "title": book.title,
            "isbn": book.isbn,
            "author": book.author,
            "year": book.year,
            "reviews": reviewDetails
        }
        return jsonify(result)

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
