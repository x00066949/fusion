from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from os import environ

from unittest.mock import patch
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from app.models import Movies
from app.main import get_movies_by_cast, get_movies_by_genre, get_movies_by_title, get_movies_by_year
from app.row_encoder import AlchemyEncoder

class TestMovies:
    def setup_class(self):
        """Setting up database connection session
        Returns a Cockroach db session for running queries against cockroach db running in same cluster
        """

        #test db data
        title_1 = 'Avengers: Age of Ultron'
        year_1 = 2015 
        extract_1 = 'Avengers: Age of Ultron is a 2015 American superhero film based on the Marvel Comics superhero team the Avengers. Produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures, it is the sequel to The Avengers (2012) and the 11th film in the Marvel Cinematic Universe (MCU). Written and directed by Joss Whedon, the film features an ensemble cast including Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans, Scarlett Johansson, Jeremy Renner, Don Cheadle, Aaron Taylor-Johnson, Elizabeth Olsen, Paul Bettany, Cobie Smulders, Anthony Mackie, Hayley Atwell, Idris Elba, Linda Cardellini, Stellan Skarsgård, James Spader, and Samuel L. Jackson. In the film, the Avengers fight Ultron (Spader)—an artificial intelligence created by Tony Stark (Downey) and Bruce Banner (Ruffalo) who plans to bring about world peace by causing human extinction.'
        thumbnail_1 = 'https://upload.wikimedia.org/wikipedia/en/f/ff/Avengers_Age_of_Ultron_poster.jpg', 
        cast_list_1 = ['Robert Downey Jr.', 'Chris Hemsworth', 'Mark Ruffalo', 'Chris Evans', 'Scarlett Johansson', 'Jeremy Renner', 'Don Cheadle', 'Aaron Taylor-Johnson', 'Elizabeth Olsen', 'Paul Bettany', 'Cobie Smulders', 'Anthony Mackie', 'Hayley Atwell', 'Idris Elba', 'Stellan Skarsgård', 'James Spader', 'Samuel L. Jackson']
        genres_1 = ['Superhero']
        thumbnail_width_1 = 220
        thumbnail_height_1 = 326    

        #setup db connection
        db_user=environ["DB_user"]
        db_password=environ["DB_PASSWORD"]    
        db_uri="cockroachdb://"+db_user+":"+db_password+"@localhost:26257/movies"
        
        engine = create_engine(db_uri)
        Session=sessionmaker(bind=engine)



    def teardown_class(self):
        self.session.rollback()
        self.session.close()

def test_setup():
    title_1 = 'Avengers: Age of Ultron'
    year_1 = 2015 
    extract_1 = 'Avengers: Age of Ultron is a 2015 American superhero film based on the Marvel Comics superhero team the Avengers. Produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures, it is the sequel to The Avengers (2012) and the 11th film in the Marvel Cinematic Universe (MCU). Written and directed by Joss Whedon, the film features an ensemble cast including Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans, Scarlett Johansson, Jeremy Renner, Don Cheadle, Aaron Taylor-Johnson, Elizabeth Olsen, Paul Bettany, Cobie Smulders, Anthony Mackie, Hayley Atwell, Idris Elba, Linda Cardellini, Stellan Skarsgård, James Spader, and Samuel L. Jackson. In the film, the Avengers fight Ultron (Spader)—an artificial intelligence created by Tony Stark (Downey) and Bruce Banner (Ruffalo) who plans to bring about world peace by causing human extinction.'
    thumbnail_1 = 'https://upload.wikimedia.org/wikipedia/en/f/ff/Avengers_Age_of_Ultron_poster.jpg', 
    cast_list_1 = ['Robert Downey Jr.', 'Chris Hemsworth', 'Mark Ruffalo', 'Chris Evans', 'Scarlett Johansson', 'Jeremy Renner', 'Don Cheadle', 'Aaron Taylor-Johnson', 'Elizabeth Olsen', 'Paul Bettany', 'Cobie Smulders', 'Anthony Mackie', 'Hayley Atwell', 'Idris Elba', 'Stellan Skarsgård', 'James Spader', 'Samuel L. Jackson']
    genres_1 = ['Superhero']
    thumbnail_width_1 = 220
    thumbnail_height_1 = 326

    title_2 = "The Strength of Donald McKenzie"
    year_2 = 1916
    extract_2 = "The Strength of Donald McKenzie is a 1916 American silent drama film directed by and starring William Russell and John Prescott. The film also stars Charlotte Burton, Harry Keenan, George Ahern, Nell Franzen, and Margaret Nichols."
    thumbnail_2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/The_Strength_of_Donald_McKenzie_%281916%29_-_1.jpg/320px-The_Strength_of_Donald_McKenzie_%281916%29_-_1.jpg"
    cast_list_2 = ["William Russell","Jack Prescott" ]
    genres_2 = ["Drama", "Silent" ]
    thumbnail_width_2 = 320
    thumbnail_height_2 = 137

    title_3 = "Fade to Black"
    year_3 = 2004
    extract_3 = "Fade to Black is a 2004 documentary film about the career of American rapper Jay-Z. It also features many other famous names in hip hop music. This live concert at Madison Square Garden was meant to be Jay-Z's final performance, as he announced his intentions to retire from the industry."
    thumbnail_3 = "https://upload.wikimedia.org/wikipedia/en/a/a8/Fade_to_Black_%282004_film%29_poster.jpg"
    cast_list_3 = [ "Jay-Z", "Beyoncé Knowles", "Mary J. Blige", "Foxy Brown", "Diddy", "Damon Dash", "Missy Elliott", "R. Kelly", "Usher", "Fonzworth Bentley", "Memphis Bleek", "Michael Buffer", "Common", "Freeway", "Funkmaster Flex", "Ghostface Killah", "Mike D", "Q-Tip", "Questlove", "Slick Rick", "Rick Rubin", "Afeni Shakur", "Beanie Sigel", "Timbaland", "Twista", "Voletta Wallace", "Kanye West", "Pharrell Williams", "Jaguar Wright" ]
    genres_3 = [ "Documentary"]
    thumbnail_width_3 = 259
    thumbnail_height_3 = 383

    movies_test_data = [Movies(title_1, year_1, extract_1, thumbnail_1, cast_list_1, genres_1, thumbnail_width_1, thumbnail_height_1),
                        Movies(title_2, year_2, extract_2, thumbnail_2, cast_list_2, genres_2, thumbnail_width_2, thumbnail_height_2),
                        Movies(title_3, year_3, extract_3, thumbnail_3, cast_list_3, genres_3, thumbnail_width_3, thumbnail_height_3)]

@patch('app.main.db_session')    
def test_get_movies_by_title(mock_db_session):
    mock_db_session.return_value = UnifiedAlchemyMagicMock()
    session = UnifiedAlchemyMagicMock()



    # Create a mock query object and configure it to return a list of users
    query = UnifiedAlchemyMagicMock()
    query.filter.return_value = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
    session.query.return_value = query

    # Call the function being tested
    result = get_movies_by_title(title='John')

    # Assert that the function returned the expected result
    assert result == [{'id': 1, 'name': 'John'}]
    # Assert that the filter method was called with the correct arguments
    query.filter.assert_called_with(Movies.title == 'John')