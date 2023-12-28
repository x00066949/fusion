from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy.orm import declarative_base

Base = declarative_base() # __init__() method is already established automatically by the declarative mapping process. 


class Movies(Base):
    """The Movies class corresponds to the "movies" database table.
    """
    __tablename__ = 'movies'
    #id = Column(UUID(as_uuid=True), primary_key=True)
    id = Column(Integer, primary_key=True, server_default=text("unique_rowid()")) # auto generated PK because no single unique attribute. Might be worth considering a composite pk  
    title = Column(String, nullable=False) 
    year = Column(Integer) 
    extract = Column(String)
    thumbnail = Column(String)
    cast_list = Column(ARRAY(String)) 
    genres = Column(ARRAY(String))  
    thumbnail_width = Column(Integer)  
    thumbnail_height = Column(Integer)

    def __init__(self, title, year, extract, thumbnail, cast_list, genres, thumbnail_width, thumbnail_height):
        self.title = title
        self.year = year
        self.extract = extract
        self.thumbnail = thumbnail
        self.cast_list = cast_list
        self.genres = genres
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height




