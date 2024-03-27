from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from api.models import Movie
from api.serializers import MovieSerializer
from api.utils import Response

# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class appStatus(APIView):
    def get(self, request):
        return Response(
            success=True,
            message="Info",
            response="Cinema Program 1.0",
            status=status.HTTP_200_OK,
        )

class MovieAPIView(APIView):
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success=True, message="Movie created successfully", response=serializer.data, status=status.HTTP_201_CREATED)
        error = {field_name: field_errors[0] if isinstance(field_errors, list) else [field_errors] for field_name, field_errors in serializer.errors.items()}
            
        return Response(success=False, message="Invalid data", response=error, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Retrieve movies from the database
        movies = Movie.objects.all()

        # Get query parameters for sorting
        sort_by = request.query_params.get('sort_by', None)
        # Sort movies based on query parameters
        if sort_by == 'name':
            movies = movies.order_by('-name')
        elif sort_by == 'ranking':
            movies = movies.order_by('-ranking')
        elif sort_by == 'status':
            movies = movies.order_by('status')
        elif sort_by == 'start_date':
            movies = movies.order_by('-start_date')

        # Serialize sorted movies
        serializer = MovieSerializer(movies, many=True)
        return Response(success=True, message="Successfully retrieved Movies", response=serializer.data, status=status.HTTP_200_OK)
