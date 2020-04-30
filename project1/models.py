from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Userdata(db.Model):
    __tablename__ = "userdata"
    username = db.Column(db.String, primary_key=True)
    passwords = db.Column(db.String, nullable=False)
    creationstamp = db.Column(db.DateTime, nullable=False)


class Books(db.Model):
    __tablename__ = "booksdata"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.String)
class Reviews(db.Model):
    _tablename_ = "reviewsdata"
    username = db.Column(db.String, primary_key = True)
    isbn = db.Column(db.String, primary_key = True)
    rating = db.Column(db.Integer, nullable = False)
    review = db.Column(db.String, nullable = False)

    def _init_(self, username, isbn, rating, review):
        self.username = username
        self.isbn = isbn
        self.rating = rating
        self.review = review