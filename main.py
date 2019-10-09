from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://isizkblnwvttxv:80a74f78b2dfac445eb358f05e6eb65ba1ae28c811b610ab3f2b6930d7d38a3d@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/de5c5roa45c8e0'
heroku = Heroku(app)
db = SQLAlchemy(app)
db.init_app(app)
from models import Movie, User, Rating

sessionID = -1

def ensure_cookie():
    global sessionID
    cook = request.cookies.get('sessionID')
    if cook is not None:
        sessionID = cook
    elif sessionID is -1:
        sessionID = str(User.query.count() + 1)
        sessionID = hashlib.md5(sessionID.encode()).hexdigest()
        db.session.add(User(sessionID))
        db.session.commit()



@app.route("/")
def home():
    ensure_cookie()
    resp = make_response(render_template("index.html"))
    resp.set_cookie('sessionID', sessionID)
    #
    #rtg = Session(561)
    #db.session.add(rtg)
    #db.session.commit()
    return resp

@app.route("/test")
def test():
    ensure_cookie()
    mov = Movie.query.get(1)
    resp = make_response(render_template("test.html", mov_id = mov.tmdb_id))
    resp.set_cookie('sessionID', sessionID)
    return resp





if __name__ == "__main__":
    app.run(debug=True)
