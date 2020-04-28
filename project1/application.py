import os
import datetime
from models import *
from create import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, request, redirect
from flask import session
from flask_session import Session
from sqlalchemy import and_

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

@app.route("/bookpage", methods = ["POST", "GET"])
def bookpage():
    if request.method == "GET":
        if not 'Email' in session:
            return render_template("register.html")
        isbn = "1416949658"
        book = Books.query.get(isbn)
        if book is None:
            return render_template("profile.html", msg = "Invalid ISBN number")
        reviews = Reviews.query.filter_by(isbn = isbn).all()
        return render_template("bookpage.html", bookDetails = book, userreviews = reviews)
    else:
        isbn = "1416949658"
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

"""
@app.route("/review", methods = ["POST"])
def addreview():
    username = request.form.get("Email").split('@')[0]
    isbn = request.form.get("isbn")
    rating = request.form.get("rating")
    review = request.form.get("review")
    
    review = Reviews(username = username, isbn = isbn, rating = rating, review = review)
    db.add(review)
    db.commit()
    return redirect(url_for("/bookpage"))
"""

def validate(uname, pwd):
    checker = db.execute("SELECT username, passwords FROM userdata WHERE username = :id and passwords= :pwd",
                         {"id": uname, "pwd": pwd}).fetchone()
    if checker is None:
        return False
    else:
        return True
