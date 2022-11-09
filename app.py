# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from create_data import Movie, Director, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create namespaces
api = Api(app)
movies_ns = api.namespace("movies")
directors_ns = api.namespace("directors")
genres_ns = api.namespace("genres")


# Create Schemas
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


# Create Movies endpoints
@movies_ns.route("/")
class MoviesViews(Resource):

    def get(self):
        # check if no args
        if not request.args:
            all_movies = db.session.query(Movie).all()
        else:
            director_id = request.args.get("director_id")
            genre_id = request.args.get("genre_id")
            # check if two args director_id and genre_id
            if director_id is not None and genre_id is not None:
                all_movies = Movie.query.filter(Movie.director_id == director_id and Movie.genre_id == genre_id).all()
            # check if one args director_id
            elif director_id is not None:
                all_movies = Movie.query.filter(Movie.director_id == director_id).all()
            # check if one args genre_id
            elif genre_id is not None:
                all_movies = Movie.query.filter(Movie.genre_id == genre_id).all()

        return movies_schema.dump(all_movies), 200

    def post(self):
        # get json from request
        req_json = request.json
        # create new row
        new_movie = Movie(**req_json)
        # add to database
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movies_ns.route("/<int:pk>")
class MovieViews(Resource):
    def get(self, pk):
        try:
            movie = db.session.query(Movie).get(pk)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, pk):
        try:
            # get json from request
            req_json = request.json
            # get element
            movie = db.session.query(Movie).get(pk)
            # update element
            movie.id = req_json.get("id")
            movie.title = req_json.get("title")
            movie.description = req_json.get("description")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get("year")
            movie.rating = req_json.get("rating")
            movie.genre_id = req_json.get("genre_id")
            movie.director_id = req_json.get("director_id")
            # add to datebase
            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, pk):
        movie = db.session.query(Movie).get(pk)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


# Create Movies endpoints
@directors_ns.route("/")
class DirectorsViews(Resource):

    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors), 200

    def post(self):
        # get json from request
        req_json = request.json
        # create new row
        new_director = Director(**req_json)
        # add to database
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@directors_ns.route("/<int:pk>")
class DirectorViews(Resource):
    def get(self, pk):
        try:
            director = db.session.query(Director).get(pk)
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, pk):
        try:
            # get json from request
            req_json = request.json
            # get element
            director = db.session.query(Director).get(pk)
            # update element
            director.id = req_json.get("id")
            director.name = req_json.get("name")
            # add to datebase
            db.session.add(director)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, pk):
        director = db.session.query(Director).get(pk)
        db.session.delete(director)
        db.session.commit()
        return "", 204


# Create Movies endpoints
@genres_ns.route("/")
class GenresViews(Resource):

    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres), 200

    def post(self):
        # get json from request
        req_json = request.json
        # create new row
        new_genre = Genre(**req_json)
        # add to database
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genres_ns.route("/<int:pk>")
class GenreViews(Resource):
    def get(self, pk):
        try:
            genre = db.session.query(Genre).get(pk)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, pk):
        try:
            # get json from request
            req_json = request.json
            # get element
            genre = db.session.query(Genre).get(pk)
            # update element
            genre.id = req_json.get("id")
            genre.name = req_json.get("name")
            # add to database
            db.session.add(genre)
            db.session.commit()
            return "", 204
        except Exception as e:
            return str(e), 404

    def delete(self, pk):
        genre = db.session.query(Genre).get(pk)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
