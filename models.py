from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from main import db

class Movie(Model):
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

class Rating(Model):
    __tablename__ = "rating"
    id =  db.Column(db.Integer,primary_key=True)
    session_id = db.Column(db.Text(), db.ForeignKey('session.session_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id') )
    rating = db.Column(db.Integer)

    def __init__(self, session, mov_id, rating):
        self.session_id = session
        self.movie_id = mov_id
        self.rating = rating

    def __repr__(self):
        return "User %s rated film %s : %s" % (self.session, self.movie_id, self.rating)


class Session(Model):
    __tablename__ = "session"
    session_id = db.Column(db.Text(), primary_key=True)

    def __init__(self, id):
        self.session_id = id

    def __repr__(self):
        return "%s" % (self.session_id)
