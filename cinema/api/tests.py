import os
import pytest
from django.conf import settings
from ninja.testing import TestClient
from cinema.api.models import Movie
from cinema.api.schemas import MovieSortBy
from cinema.cinema import api  # Assuming 'cinema' is the name of the file where the NinjaAPI instance is defined

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

@pytest.fixture
def client():
    return TestClient(api)

@pytest.mark.django_db
def test_app_status(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Info",
        "response": "Cinema Program 1.0",
        "status": 200
    }

@pytest.mark.django_db
def test_get_movie_by_id(client):
    # Add a movie to the database for testing
    movie = Movie.objects.create(name="Test Movie", protagonists=["Actor 1", "Actor 2"], status="starting", start_date="2024-03-20", ranking=5)

    # Send a GET request to retrieve the movie by ID
    response = client.get(f"/movies/{movie.id}")
    assert response.status_code == 200  # Assuming success status code is 200

    # Check if the movie data matches the expected data
    movie_data = response.json()["response"]
    assert movie_data["name"] == "Test Movie"
    # Add more assertions for other fields if needed

@pytest.mark.django_db
def test_get_all_movies(client):
    # Send a GET request to retrieve all movies
    response = client.get("/movies", params={"sort_by": MovieSortBy.name.value})
    assert response.status_code == 200  # Assuming success status code is 200

    # Check if the response contains a list of movies
    movies = response.json()["response"]
    assert isinstance(movies, list)
    # Add more assertions if needed
