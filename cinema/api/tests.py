from ninja.testing import TestClient
from api.models import Movie
from api.schemas import MovieSortBy
from ..cinema import api  # Assuming 'main' is the name of the file where the NinjaAPI instance is defined
import pytest

@pytest.fixture
def client():
    return TestClient(api)

def test_add_movie(client):
    # Prepare payload for adding a movie
    payload = {
        "name": "Test Movie",
        "protagonists": ["Actor 1", "Actor 2"],
        "status": "starting",
        "start_date": "2024-03-20",
        "ranking": 5
    }

    # Send a POST request to add the movie
    response = client.post("/movies", data=payload)
    assert response.status_code == 200  # Assuming success status code is 200

    # Check if the movie was added successfully
    movie_data = response.json()["response"]
    assert movie_data["name"] == "Test Movie"
    # Add more assertions for other fields if needed

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

def test_get_all_movies(client):
    # Send a GET request to retrieve all movies
    response = client.get("/movies", params={"sort_by": MovieSortBy.name.value})
    assert response.status_code == 200  # Assuming success status code is 200

    # Check if the response contains a list of movies
    movies = response.json()["response"]
    assert isinstance(movies, list)
    # Add more assertions if needed
