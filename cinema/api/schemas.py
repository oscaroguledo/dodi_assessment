import re, uuid
from enum import Enum
from ninja import Schema, FilterSchema, Field 
from typing import List, Optional, Union
from ninja.responses import Response as NinjaResponse
from ninja import NinjaAPI, Query, UploadedFile,File
from datetime import date, datetime


class MovieFilterSchema(FilterSchema):
    name: Optional[str] = Field(q="name__icontains")
    status: Optional[str] = Field(q="status__icontains")
    ranking: Optional[int] = Field(q="ranking__gte")
    start_date: Optional[date] = Field(q="start_date__gte")


class MovieSortBy(Enum):
    name = "name"
    ranking = "ranking"
    status = "status"
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
    poster: Optional[Union[str, bytes]]
    trailer: Optional[str]

    
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
        print(data)
        try:
            self.validate_name(data['name'])
            self.validate_start_date(data['start_date'])
        except ValueError as e:
            return {'success': False, 'error': str(e)}
        return {'success': True}











class InvalidResponseDataError(Exception):
    def __str__(self):
        return "\033[91m" + str(self.args[0]) + "\033[0m"

class Response(NinjaResponse):
    def __init__(self, success=None, message=None, response=None, status=None):
        if success not in (True, False):
            raise InvalidResponseDataError("success value must be either True or False")
        if message is None:
            raise InvalidResponseDataError("message value cannot be None")
        if status is None:
            status = 200
        
        self.success = success
        self.message = message
        self.response = response
        self.status = status
        data = {"success": success, "message": message}
        if response:
            data['response']=response
        super().__init__(data, status=status)
