from flask import Flask, jsonify
from types import SimpleNamespace

import logging
import json
from os import environ

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.dialects import postgresql


from models import Movies
from row_encoder import AlchemyEncoder


app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def db_session():
    """Setting up database connection session
    Returns a Cockroach db session for running queries against cockroach db running in same cluster
    """
    db_user=environ["DB_USER"]
    db_password=environ["DB_PASSWORD"]

    logging.info("connecting to db")    
    db_uri="cockroachdb://"+db_user+":"+db_password+"@my-release-cockroachdb-public.default.svc.cluster.local:26257/movies"

    #in a real production environment, i'd opt for ssl cert auth (over username+password auth) in which case, the uri would be:
    #db_uri="cockroachdb://my-release-cockroachdb-public.default.svc.cluster.local:26257/movies?sslmode=require&sslrootcert=/cockroach/cockroach-certs/client.root.crt&sslcert=/cockroach/cockroach-certs/ca.crt&sslkey=/cockroach/cockroach-certs/client.root.key"
    
    try:        
        engine = create_engine(db_uri)
    except Exception as e:
        logging.info("Failed to connect to database.")
        logging.info(f"{e}")
    
    logging.info("connected to db")

    Session=sessionmaker(bind=engine)
    return Session()

@app.route("/", methods=["GET"])
def hello():
    db_session()
    return "Welcome to the Movies Data API"

@app.route('/year/<int:year>', methods=["GET"])
def get_movies_by_year(year):
    """Find movies released in a given year
    """

    session = db_session()    

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

    session = db_session()

    try:
        result = session.query(Movies).filter(Movies.title.icontains(title)).all()
    except NoResultFound:
        logging.info("No result was found")
    except MultipleResultsFound:
        logging.info("Multiple results were found")
        logging.info(result)

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

    session = db_session()

    result = session.query(Movies).filter(Movies.cast_list.contains([full_name])).all()    
    result_dict = json.dumps(result, cls=AlchemyEncoder)
    
    return result_dict

@app.route('/genre/<genre>', methods=["GET"])
def get_movies_by_genre(genre):
    """get movies in a specified genre
    Works  for cast with Singlename, Firstname Surname and Firstname Middlename Surname only. 
    I am aware that this won't work for cast more that 3 names or if capitalization is in the middle. 
    (There is room for improvement here. Can improve the query so the query returns case insensitive result)
    """

    session = db_session()   

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
    this is mostly used to load test data initially so will only br run once to allow us to run queries against our local cluster
    """
    movie_file = open('movies.json')
    movies_data = json.load(movie_file)
    movie_rows = []

    for movie in movies_data:
        x = json.loads(json.dumps(movie), object_hook=lambda d: SimpleNamespace(**d))   # Parse JSON into an object with attributes corresponding to dict keys.

        row = assign_column(x)
        movie_rows.append(row)

        logging.info('%s added to db',x.title )
    
    session = db_session()

    session.add_all(movie_rows)   
    session.commit()

    return "ok"
if __name__ == "__main__":
    app.run(host='0.0.0.0')