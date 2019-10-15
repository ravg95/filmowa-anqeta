from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import sys
import json
from flask import jsonify
from flask_heroku import Heroku
from flask_cors import CORS, cross_origin
import tmdbsimple as tmdb

tmdb.API_KEY = 'b5e95273c3bc67794bffa473d3439747'

poster_path= "https://image.tmdb.org/t/p/original"
imdb_path = "https://www.imdb.com/title/"

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://isizkblnwvttxv:80a74f78b2dfac445eb358f05e6eb65ba1ae28c811b610ab3f2b6930d7d38a3d@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/de5c5roa45c8e0'
heroku = Heroku(app)
db = SQLAlchemy(app)
db.init_app(app)
from models import Movie, User, Rating

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cookieId = -1

def checkUser(cookie):
    ww = User.query.filter(User.session_id.match(cookie)).first()
    if ww is None:
        db.session.add(User(cookie))
        db.session.commit()
        return True
    else:
        return False


@app.route("/user", methods = ['GET'])
@cross_origin()
def user():
    global cookieId
    #cookieId = request.headers.get('Authorization')
    cookieId = '18baab70-ef36-11e9-af39-f94d7c840094'
    if checkUser(cookieId):
        return jsonify(
            firstMovieId = 1,
            nextMovieId = 1
        )
    else:
        mov = db.session.query(func.max(Rating.movie_id).filter(Rating.session_id==cookieId)).one()[0]
        return jsonify(
            firstMovieId = 1,
            nextMovieId = mov + 1
        )


@app.route("/movie/<int:id>", methods = ['GET'])
@cross_origin()
def getMovie(id):
    #cookieId = request.headers.get('Authorization')
    cookieId = '18baab70-ef36-11e9-af39-f94d7c840094'
    checkUser(cookieId)
    mv = tmdb.Movies(Movie.query.get(id).tmdb_id)
    response = mv.info()
    prevId = id - 1
    if prevId < 1:
        prevId = None
    nextId = id + 1
    if nextId > 200:
        nextId = None
    resp2 = mv.credits()
    drs = [credit for credit in mv.crew if credit["job"] == "Director"]
    directors = []
    for dr in drs:
        directors.append(dr['name'])
    actors = []
    for actor in mv.cast[0:3]:
        actors.append(actor['name'])
    row = Rating.query.filter_by(session_id = cookieId, movie_id = id).first()
    hasVoted = (row != None)
    if hasVoted:
        vote = row.rating
    else:
        vote = None

    cnt = Rating.query.filter_by(session_id = cookieId).count()

    d = {
      'title': mv.title,
      'plot': mv.overview,
      'director': directors,
      'actors': actors,
      'imdb_url': imdb_path + mv.imdb_id,
      'poster_url': poster_path + mv.poster_path,
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
    #cookieId = request.headers.get('Authorization')
    cookieId = '18baab70-ef36-11e9-af39-f94d7c840094'
    checkUser(cookieId)
    json_data = request.get_json()
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
