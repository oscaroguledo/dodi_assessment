from ninja import Query, UploadedFile,File, Form
from .models import Movie, models
from movies.schemas import MovieSchema, MovieSortBy, MovieSorting
from typing import List
import uuid, datetime
from movies.utils import Response
from ninja import Router

router = Router()

@router.post("/")
def add(request, payload: MovieSchema = Form(...), poster: UploadedFile = File(...),trailer: UploadedFile = File(...)):
    validation_result = payload.is_valid(payload.dict())

    if not validation_result['success']:
        return Response(success=False, message="Invalid data",response=validation_result['error'],status=400)
        
    movie= Movie.objects.filter(name=payload.name)
    if movie:
        return Response(
            success=False,
            message="Movie already exists",
            response={"id":movie[0].id,"name":movie[0].name},
            status=400
        )
        
    # Create the Movie instance
    movie_instance = Movie(
        name=payload.name, 
        protagonists=list(payload.protagonists[0].split(",")),
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
        response={"id":movie_instance.id,"name":movie_instance.name},
        status=200
    )

@router.get("/{var}")
def get_movie(request, var: str):
    # Retrieve movie from the database
    try:
        # Try to create a UUID object
        var = uuid.UUID(var)
    except Exception as e:
        try:
            var=eval(var)
        except Exception as e:
            pass
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
        
@router.get("/", response=List[MovieSchema])
def get_movies(request, sort_by: MovieSorting = Query(...)):
    # Retrieve movies from the database
    movies = Movie.objects.exclude(ranking__isnull=True).values('id', 'name', 'protagonists', 'status', 'start_date', 'poster', 'trailer', 'ranking')
        
    # Sort movies based on query parameters
    if sort_by == MovieSortBy.name:
        movies = movies.order_by('name')
    elif sort_by == MovieSortBy.ranking:
        movies = movies.order_by('-ranking')
    elif sort_by == MovieSortBy.start_date:
        movies = movies.order_by('-start_date')

    return Response(success=True, message="Successfully retrieved Movies", response=list(movies), status=200)
    
@router.put("/{id}")
def update_movie(request, id:uuid.UUID, payload: MovieSchema = Form(...), poster: UploadedFile = File(...),trailer: UploadedFile = File(...) ):
    print('============================pplkongbvfb')
    validation_result = payload.is_valid(payload.dict())

    if not validation_result['success']:
        return Response(success=False, message="Invalid data",response=validation_result['error'],status=400)
        
    movie = Movie.objects.get(id=id)
    if not movie:
        return Response(success=False,message="Movie not found",response=None,status=404)
    print(movie,'||||||||||||||||||||||||||')
    movie.save()
    return Response(success=True,message="Movie updated successfully",response=None,status=200)

@router.delete("/{id}")
def delete_movie(request,id:uuid.UUID):
    print(id, "---",type(id))
    movie = Movie.objects.filter(id=id)
    if not movie:
        return Response(success=False,message="Movie not found",response=None,status=404)
    movie.delete()
    return Response(success=True,message="Movie deleted successfully",response=None,status=200)
        
