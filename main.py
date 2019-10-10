from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
import hashlib
import tmdbsimple as tmdb

tmdb.API_KEY = 'b5e95273c3bc67794bffa473d3439747'

poster_path= "https://image.tmdb.org/t/p/original/"

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
    return resp

@app.route("/test")
def test():
    ensure_cookie()
    i=0
    movies = []
    for j in range(5):
        mv = tmdb.Movies(Movie.query.get(5*i+1+j).tmdb_id)
        response = mv.info()
        movies.append(MovieInfo(5*i+1+j, mv.title, poster_path + mv.poster_path, mv.original_title, mv.overview, mv.release_date))

    resp = make_response(render_template("test.html", movies = movies))
    resp.set_cookie('sessionID', sessionID)
    return resp

class MovieInfo:
    id: int
    title:  str
    image_src: str
    original_title: str
    overview: str
    release_date: str
    def __init__(self, id, title, image_src, original_title, overview, release_date):
        self.id = id
        self.title = title
        self.image_src = image_src
        self.original_title = original_title
        self.overview = overview
        self.release_date = release_date

if __name__ == "__main__":
    app.run(debug=True)
