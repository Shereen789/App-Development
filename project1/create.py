import os
from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
#print(os.getenv("DATABASE_URL"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()

#postgres://grsnhnmpbgqmax:93c7669b3dc11b1a14663d42eacc0febf80c93d01ff07a78722453e031f0ef99@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d632pf2fn65rt6