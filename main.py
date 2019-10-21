from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import sys
import json
from flask import jsonify
from flask_heroku import Heroku
from flask_cors import CORS, cross_origin
from flask import abort
import os
db_url = os.environ.get('DATABASE_URL')

poster_path= "https://image.tmdb.org/t/p/original"
imdb_path = "https://www.imdb.com/title/"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
heroku = Heroku(app)
db = SQLAlchemy(app)
db.init_app(app)
from models import Movie, User, Rating, MovieInfo

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def checkUser(cookie):
    ww = User.query.filter(User.session_id.match(cookie)).first()
    if ww is None:
        db.session.add(User(cookie))
        db.session.commit()
        return True
    else:
        return False
@app.route("/")
@cross_origin()
def main():
    return str(db_url)

@app.route("/user", methods = ['GET'])
@cross_origin()
def user():
    cookieId = request.headers.get('Authorization')
    #cookieId = '18baab70-ef36-11e9-af39-f94d7c840094'
    if checkUser(cookieId):
        return jsonify(
            firstMovieId = 1,
            nextMovieId = None
        )
    else:
        mov = db.session.query(func.max(Rating.movie_id).filter(Rating.session_id==cookieId)).one()[0]
        if mov is not None:
            mov +=1
        return jsonify(
            firstMovieId = 1,
            nextMovieId = mov
        )


@app.route("/movie/<int:id>", methods = ['GET'])
@cross_origin()
def getMovie(id):
    cookieId = request.headers.get('Authorization')
    #cookieId = '18baab70-ef36-11e9-af39-f94d7c840094'
    checkUser(cookieId)
    mov = db.session.query(func.max(Rating.movie_id).filter(Rating.session_id==cookieId)).one()[0]
    if (mov is not None and id > mov+1) or (mov is None and id > 1):
        abort(404)
    mv = MovieInfo.query.get(id)
    prevId = id - 1
    if prevId < 1:
        prevId = None
    nextId = id + 1
    if nextId > 200:
        nextId = None

    row = Rating.query.filter_by(session_id = cookieId, movie_id = id).first()
    hasVoted = (row != None)
    if hasVoted:
        vote = row.rating
    else:
        vote = None

    cnt = Rating.query.filter_by(session_id = cookieId).count()
    d = {
      'title': mv.title,
      'original_title': mv.original_title,
      'plot': mv.plot,
      'director': eval(mv.director),
      'actors': eval(mv.actors),
      'imdb_url': mv.imdb_url,
      'poster_url': mv.poster_url,
      'hasVoted': hasVoted,
      'vote': vote
    }
    return jsonify(
      nextMovieId = nextId,
      currentMovieId = id,
      previousMovieId = prevId,
      movie = d,
      ratedMoviesCount = cnt
    )


@app.route("/movie/<int:id>/vote", methods = ['POST'])
@cross_origin()
def vote(id):
    cookieId = request.headers.get('Authorization')
    #cookieId = '18baab70-ef36-11e9-af39-f94d7c840094'
    checkUser(cookieId)
    json_data = request.get_json(force=True)
    vote = json_data['vote']
    row = Rating.query.filter_by(session_id = cookieId, movie_id = id).first()
    hasVoted = (row != None)
    if hasVoted:
        row.rating = vote
        db.session.commit()
    else:
        rating = Rating(cookieId, id, vote)
        db.session.add(rating)
        db.session.commit()
    return ""



if __name__ == "__main__":
    app.run(debug=True)
