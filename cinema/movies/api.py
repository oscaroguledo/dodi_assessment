from ninja import Query, UploadedFile,File, Form
from .models import Movie, models
from movies.schemas import MovieSchema,UpdateMovieSchema, MovieSortBy, MovieSorting
from typing import List, Optional
import uuid, datetime
from movies.utils import Response
from ninja import Router
from django.core.files.storage import default_storage
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
    
@router.patch("/update/{id}")
def update_movie(request, id: uuid.UUID, payload: UpdateMovieSchema = Form(...)):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(success=False, message="Movie not found", response=None, status=404)
    if len(request.body) > 0:
        data = request.body.decode('utf-8')
    payload.populate_originals(movie)
    # Update movie fields based on payload (as before)
    for field, value in payload.dict().items():
        if value is not None:
            validation_result = payload.is_valid(payload.dict())
            if not validation_result['success']:
                return Response(success=False, message="Invalid data", response=validation_result['error'], status=400)
            try:
                patch_value = data[len(field)+data.index(field)+1:data.index("&")]
                if len(patch_value) > 0:
                    if field == 'name':
                        movie.name=patch_value
                    elif field == 'protagonists':
                        movie.protagonists=list(patch_value.split(","))
                    elif field =='status':
                        movie.status=patch_value
                    elif field == 'ranking':
                        movie.ranking=patch_value
                    elif field =='start_date':
                        movie.start_date=payload._date(patch_value)
                    elif field == 'poster':
                        movie.poster = payload.poster
                    elif field == 'trailer':
                        movie.trailer = payload.trailer
                    else:
                        movie.field=patch_value
            except Exception as e:
                pass
    movie.save()

    return Response(success=True,message="Movie updated successfully",response=None,status=200)

@router.delete("/delete/{id}")
def delete_movie(request,id:uuid.UUID):
    print(id, "---",type(id))
    movie = Movie.objects.filter(id=id)
    if not movie:
        return Response(success=False,message="Movie not found",response=None,status=404)
    movie.delete()
    return Response(success=True,message="Movie deleted successfully",response=None,status=200)
        
