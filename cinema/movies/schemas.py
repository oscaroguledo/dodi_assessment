import re, uuid
from enum import Enum
from ninja import Schema, FilterSchema, Field 
from typing import List, Optional, Union

from ninja import NinjaAPI, Query, UploadedFile,File
from datetime import date, datetime


class MovieSortBy(Enum):
    name = "name"
    ranking = "ranking"
    start_date = "start_date"

class MovieSorting(Schema):
    sort_by: MovieSortBy = MovieSortBy.name

class MovieStatus(str, Enum):
    coming_up = "coming-up"
    starting = "starting"
    running = "running"
    finished = "finished"

class MovieSchema(Schema):
    name: str = Field(..., unique=True)
    protagonists: List[str]
    ranking: Optional[int]
    status: MovieStatus
    start_date: str
    
    def validate_name(self, value):
        if not value or len(value) > 255:
            raise ValueError("Name must be between 1 and 255 characters")

    def _date(self, d):
        return datetime.strptime(d,"%Y-%m-%d")
    def validate_start_date(self, d):
        
        try:
            
            value = self._date(d)
            if len(d) != 10:
                print(d,"=================")
                raise ValueError("Date must be in YYYY-MM-DD format")
        
        except (AttributeError, ValueError) as e:
            raise ValueError(e)

    def is_valid(self, data):
        try:
            self.validate_name(data['name'])
            self.validate_start_date(data['start_date'])
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        return {'success': True}



class UpdateMovieSchema(Schema):
    name: Optional[str] = None
    protagonists: Optional[List[str]] = None
    ranking: Optional[int] = None
    status: Optional[MovieStatus] = None
    start_date: Optional[str] = None
    poster: Union[None, UploadedFile] = None
    trailer: Union[None, UploadedFile] = None

    def populate_originals(self, movie):
        # Access the movie object from context
        if movie:
            self.name = movie.name if self.name is None else self.name
            self.protagonists = movie.protagonists if self.protagonists is None else self.protagonists
            self.ranking = movie.ranking if self.ranking is None else self.ranking
            self.status = movie.status if self.status is None else self.status
            self.start_date = str(movie.start_date) if self.start_date is None else self.start_date
            self.poster = movie.poster if self.poster is None else self.poster
            self.trailer = movie.trailer if self.trailer is None else self.trailer

    def validate_name(self, value):
        if not value or len(value) > 255:
            raise ValueError("Name must be between 1 and 255 characters")

    def _date(self, d):
        return datetime.strptime(d,"%Y-%m-%d")
    def validate_start_date(self, d):
        try:
            value = self._date(d)
            if len(d) != 10:
                raise ValueError("Date must be in YYYY-MM-DD format")
        
        except (AttributeError, ValueError) as e:
            raise ValueError(e)

    def is_valid(self, data):
        try:
            self.validate_name(data['name'])
            self.validate_start_date(data['start_date'])
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        return {'success': True}

