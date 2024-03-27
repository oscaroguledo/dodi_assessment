from ninja import NinjaAPI, Query, UploadedFile,File, errors, Form
from api.models import Movie, models
from api.schemas import MovieSchema, Response, MovieFilterSchema,MovieSortBy, MovieSorting
from typing import List
import uuid, json, datetime

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
    @api.post("/movies")
    def add(request, payload: MovieSchema = Form(...), poster: UploadedFile = File(...),trailer: UploadedFile = File(...)):
        validation_result = payload.is_valid(payload.dict())

        if not validation_result['success']:
            return Response(success=False, message="Invalid data",response=validation_result['error'],status=400)
        
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
            poster = poster,
            trailer = trailer,
            start_date=payload._date(payload.start_date),  
        )
        movie_instance.save()

        # Access file data from the UploadedFile objects
        return Response(
            success=True,
            message="Movie added successfully",
            response=MovieSchema.from_orm(movie_instance),
            status=200
        )

    @api.get("/movies/{var}")
    def get_movie(request, var: str):
        # Retrieve movie from the database
        if isinstance(var, uuid.UUID):
            movie = Movie.objects.filter(id=var).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')
        elif isinstance(var, str):
            st_date=None
            try:
                st_date = datetime.datetime.strptime(var,"%Y-%m-%d")
                movie = Movie.objects.filter(models.Q(start_date=st_date)|models.Q(name=var) | models.Q(name=var) | models.Q(protagonists__icontains=var)| models.Q(status=var)).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')
            except Exception:
                movie = Movie.objects.filter(models.Q(start_date=st_date)|models.Q(name=var) | models.Q(name=var) | models.Q(protagonists__icontains=var)| models.Q(status=var)).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')
        elif isinstance(var, int):
            movie = Movie.objects.filter(ranking=var).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')
        else:
           movie = Movie.objects.filter(id=None).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')

        if not movie:
            return Response(success=False,message="Movie not found",response=None,status=404)
        return Response(success=True,message="Movie retrieved successfully",response=list(movie),status=200)
        
    @api.get("/movies", response=List[MovieSchema])
    def get_movies(request, sort_by: MovieSorting = Query(...)):
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
    
    @api.patch("/movies/{var}")
    def patch_movie(request, var:uuid.UUID, payload:MovieSchema):
        movie = Movie.objects.get(id=var)
        if not movie:
            return Response(success=False,message="Movie not found",response=None,status=404)
        for attr, value in payload.dict().items():
            setattr(movie, attr, value)
        movie.save()
        return Response(success=True,message="Movie updated successfully",response=None,status=200)

    @api.delete("/movies/{var}")
    def delete_movie(request, var:uuid.UUID):
        movie = Movie.objects.filter(id=var)
        if not movie:
            return Response(success=False,message="Movie not found",response=None,status=404)
        movie.delete()
        return Response(success=True,message="Movie deleted successfully",response=None,status=200)
        
