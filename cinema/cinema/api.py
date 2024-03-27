from ninja import NinjaAPI, Query, UploadedFile,File, errors
from api.models import Movie, models
from api.schemas import MovieSchema, Response, MovieFilterSchema,MovieSortBy, MovieSorting
from typing import List
import uuid, json

api = NinjaAPI()

@api.get("/")
def app_status(request):
    return Response(
        success=True,
        message="Info",
        response="Cinema Program 1.0",
        status=200,
    )

class MovieApi:
    @api.post("/movies", response=MovieSchema)
    def add(request, payload: MovieSchema):
        
        validation_result = payload.is_valid(payload.dict())

        if not validation_result['success']:
            return Response(
                success=False,
                message="Invalid data",
                response=validation_result['error'],
                status=400
            )
        movie= Movie.objects.get(name=payload.name)
        if movie:
            return Response(
                success=False,
                message="Movie already exists",
                response={"id":movie.id,"name":movie.name},
                status=400
            )
        
        # Create the Movie instance
        movie_instance = Movie(
            name=payload.name, 
            protagonists=payload.protagonists,
            ranking=payload.ranking,
            status=payload.status,
            start_date=payload._date(payload.start_date),  
        )
        movie_instance.save()

        return Response(
            success=True,
            message="Movie added successfully",
            response=MovieSchema.from_orm(movie_instance),
            status=200
        )

    @api.get("/movies/{id}")
    def get_id(request, id: uuid.UUID):
        # Retrieve movie from the database
        
        movie = Movie.objects.filter(id=id).values('id', 'name', 'protagonists', 'status', 'status', 'start_date', 'poster', 'trailer', 'ranking')
        if not movie:
            return Response(
                success=False,
                message="Movie not found",
                response=None,
                status=404
            )
        return Response(success=True,message="Movie retrieved successfully",response=list(movie),status=200)
        
    @api.get("/movies", response=List[MovieSchema])
    def get_all(request, sort_by: MovieSorting = Query(...)):
        # Retrieve movies from the database
        movies = Movie.objects.exclude(ranking__isnull=True).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')
        

        # Sort movies based on query parameters
        if sort_by == MovieSortBy.name:
            movies = movies.order_by('-name')
        elif sort_by == MovieSortBy.ranking:
            movies = movies.order_by('-ranking')
        elif sort_by == MovieSortBy.status:
            movies = movies.order_by('status')
        elif sort_by == MovieSortBy.start_date:
            movies = movies.order_by('-start_date')

        print(list(movies))
        return Response(success=True, message="Successfully retrieved Movies", response=list(movies), status=200)

