from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
import datetime
from main import db

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.Text())

    def __init__(self, id, tmdb_id, title):
        self.id = id
        self.tmdb_id = tmdb_id
        self.title = title

    def __repr__(self):
        return "%s (%s): %s" % (self.id, self.tmdb_id, self.title)

class Rating(db.Model):
    __tablename__ = "rating"
    id =  db.Column(db.Integer,primary_key=True)
    session_id = db.Column(db.Text(), db.ForeignKey('session.session_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id') ,nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    __table_args__ = (UniqueConstraint('session_id', 'movie_id', name='unik'),)

    def __init__(self, session, mov_id, rating):
        self.session_id = session
        self.movie_id = mov_id
        self.rating = rating

    def __repr__(self):
        return "User %s rated film %s : %s" % (self.session_id, self.movie_id, self.rating)


class User(db.Model):
    __tablename__ = "session"
    session_id = db.Column(db.Text(), primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id):
        self.session_id = id

    def __repr__(self):
        return "%s" % (self.session_id)

class MovieInfo(db.Model):
    __tablename__ = "info"
    id = db.Column(db.Integer, primary_key=True)
    title=  db.Column(db.Text())
    original_title=  db.Column(db.Text())
    plot=  db.Column(db.Text())
    director=  db.Column(db.Text())
    actors=  db.Column(db.Text())
    imdb_url=  db.Column(db.Text())
    poster_url=  db.Column(db.Text())

    def __init__(self, id, title, original_title, plot, director, actors, imdb_url, poster_url):
        self.id = id
        self.title = title
        self.original_title = original_title
        self.plot = plot
        self.director = director
        self.actors = actors
        self.imdb_url = imdb_url
        self.poster_url = poster_url
