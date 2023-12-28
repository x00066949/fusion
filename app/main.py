from flask import Flask
from types import SimpleNamespace

import json
from os import environ
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from __init__ import get_db
from models import Movies
from row_encoder import AlchemyEncoder


app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@app.route("/", methods=["GET"])
def hello():
    get_db()
    return "Welcome to the Movies Data API"

@app.route('/year/<int:year>', methods=["GET"])
def get_movies_by_year(year):
    """Find movies released in a given year
    """

    session = get_db() 

    result = session.query(Movies).filter(Movies.year == year).all()
    result_dict = json.dumps(result, cls=AlchemyEncoder)
    
    return result_dict


@app.route('/title/<title>', methods=["GET"])
def get_movies_by_title(title):
    """Find movie info given a title
    I am working off the assumption that, 
    - the client can search by substring. So /avengers will return all movies with Avengers in title
    - the client can search for movies with multiple words in title by replacing spaces with underscores /the_dark_knight_rises
    - case insensitive matching
    """

    title=title.replace("_", " ")

    session = get_db() 

    try:
        result = session.query(Movies).filter(Movies.title.icontains(title)).all()
    except NoResultFound:
        logging.info("No result was found")
    except MultipleResultsFound:
        logging.info("Multiple results were found")

    result_dict = json.dumps(result, cls=AlchemyEncoder)

    return result_dict

@app.route('/cast/fullname/<first>', defaults={'last': '','middle':''}, methods=["GET"])
@app.route('/cast/firstname/<first>/lastname/<last>', defaults={'middle': ''}, methods=["GET"])
@app.route('/cast/firstname/<first>/middlename/<middle>/lastname/<last>', methods=["GET"])
def get_movies_by_cast(first,middle, last):
    """get movies starring given cast member
    Works  for cast with Singlename, Firstname Surname and Firstname Middlename Surname only. 
    for more than 3 words in name, use /cast/fullname/full_name and replace spaces with underscores(_)
    I am aware that this won't work for cast more that 3 names or if capitalization is in the middle. (YahyavAbdul-Mateen II)
    (There is room for improvement here. Can improve the query so the query returns case insensitive result)
    """
    if middle != '':
        middle = ' '+middle.capitalize()

    if last != '':
        last = ' '+last.capitalize()
    
    first = first.replace("_", " ")

    full_name=first.capitalize()+middle+last

    logging.info(full_name)

    session = get_db() 

    result = session.query(Movies).filter(Movies.cast_list.contains([full_name])).all()    
    result_dict = json.dumps(result, cls=AlchemyEncoder)
    
    return result_dict

@app.route('/genre/<genre>', methods=["GET"])
def get_movies_by_genre(genre):
    """get movies in a specified genre
    """

    session = get_db()   

    result = session.query(Movies).filter(Movies.genres.contains([genre.capitalize()])).all()
    result_dict = json.dumps(result, cls=AlchemyEncoder)
    
    return result_dict


def assign_column(raw_movie_object):
    """a function to set a column to null if it doesnt exist in the raw json
    title is always expected to be present
    """
    title=raw_movie_object.title

    try:
        year=raw_movie_object.year
    except AttributeError:
        year= None

    try:
        extract=raw_movie_object.extract
    except AttributeError:
        extract= None

    try:
        thumbnail=raw_movie_object.thumbnail
    except AttributeError:
        thumbnail= None

    try:
        cast_list=raw_movie_object.cast
    except AttributeError:
        cast_list= None

    try:
        genres=raw_movie_object.genres
    except AttributeError:
        genres= None

    try:
        thumbnail_width=raw_movie_object.thumbnail_width
    except AttributeError:
        thumbnail_width= None

    try:
        thumbnail_height=raw_movie_object.thumbnail_height
    except AttributeError:
        thumbnail_height= None      

    return Movies(title=title, year=year, extract=extract, thumbnail=thumbnail, cast_list=cast_list, genres=genres, thumbnail_width=thumbnail_width, thumbnail_height=thumbnail_height)


@app.route('/addall', methods=["GET"])
def add_movies():
    """ a function that adds all movies from movies.json to a CockroachDB table
    this is used to load test data initially so will only br run once to allow us to run queries against our local cluster
    """
    movie_file = open('movies.json')
    movies_data = json.load(movie_file)
    movie_rows = []

    for movie in movies_data:
        x = json.loads(json.dumps(movie), object_hook=lambda d: SimpleNamespace(**d))   # Parse JSON into an object with attributes corresponding to dict keys.

        row = assign_column(x)
        movie_rows.append(row)

        logging.info('adding %s to db',x.title )
    
    session = get_db() 

    session.add_all(movie_rows)   
    session.commit()

    return "ok"
if __name__ == "__main__":
    app.run(host='0.0.0.0')