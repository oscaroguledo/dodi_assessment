from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ninja.testing import TestClient
from ninja import errors
from .models import Movie
from .schemas import MovieStatus
from .api import router  # Assuming your API is defined in movies.api
import django, os
from datetime import datetime
import pytest
from io import BytesIO
from uuid import uuid4
from .tasks import increase_movie_ranking

django.setup()  # Call before accessing any settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema.settings')

# Now you can access settings like:
DEBUG = django.conf.settings.DEBUG


@pytest.fixture
def client():
    return TestClient(router)


@pytest.mark.django_db
def test_add_movie_success(client, db):
        # Define valid movie data
        data = {
            "name": "Test Movie",
            "protagonists": '["John Doe", "Jane Doe"]',
            "ranking": 4,
            "status": "coming-up",  # Assuming this is a valid status choice
            "start_date": "2024-03-30",  # Adjust date format as needed
        }

        # Send POST request with multipart form data
        response = client.post("/", data=data, FILES={
            "poster": SimpleUploadedFile("poster.jpg", b"poster_content", content_type="image/jpeg"),
            "trailer": SimpleUploadedFile("trailer.mp4", b"trailer_content", content_type="video/mp4"),
        })

        # Assert response status and data
        print(response.json(), response.status_code, response)
        assert(response.status_code,200)
        assert(response.json()['success'],True)
@pytest.mark.django_db
def test_add_movie_invalid_data(client, db):
        # Send POST request with missing field
        data = {
            "name": "Test Movie",
            "protagonists": '["John Doe", "Jane Doe"]',
            "ranking": 4,
            "status": "coming-up",  # Assuming this is a valid status choice
            "start_date": "2024-003-30",  # Adjust date format as needed
        }

        # Send POST request with multipart form data
        response = client.post("/", data=data, FILES={
            "poster": SimpleUploadedFile("poster.jpg", b"poster_content", content_type="image/jpeg"),
            "trailer": SimpleUploadedFile("trailer.mp4", b"trailer_content", content_type="video/mp4"),
        })
        # Assert error response
        print(response, response.status_code)
        assert(response.status_code,400)
        assert(response.json()['success'],True)
@pytest.mark.django_db
def test_add_movie_duplicate_name(client,db):
        # Create a movie with the same name beforehand
        
        existing_movie = Movie.objects.create(
            name="Duplicate Movie",
            protagonists=["John Doe", "Jane Doe"],
            ranking=4,
            status="coming-up",
            start_date=datetime(2024, 3, 30),
            # Consider uploading dummy files for posters and trailers if needed
            # poster="poster.jpg",
            # trailer="trailer.mp4"
            # ... other movie data
        )

        # Send POST request with duplicate name
        response = client.post("/", data={
            "name": existing_movie.name,
            "protagonists": '["John Doe, Jane Doe"]',
            "ranking": 4,
            "status": "coming-up",
            "start_date": "2024-03-30",  # Adjust date format as needed
        },FILES={
            "poster": SimpleUploadedFile("poster.jpg", b"poster_content", content_type="image/jpeg"),
            "trailer": SimpleUploadedFile("trailer.mp4", b"trailer_content", content_type="video/mp4"),
        })

        # Assert duplicate error response
        print(response.json(),"==================")
        assert(response.status_code,400)
        assert(response.json()['success'],True)

        # Clean up by deleting the created movie
        existing_movie.delete()

@pytest.mark.django_db
def test_get_movie_by_id(client, db):
    # Create a movie for testing
    movie_id = uuid4()
    Movie.objects.create(
        id=movie_id,
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )

    response = client.get(f"/{movie_id}")
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 1  # Expecting one movie in the response
    assert response.json()["response"][0]["name"] == "Test Movie"

@pytest.mark.django_db
def test_get_movie_by_id_not_found(client, db):
    # Create a movie for testing
    movie_id = uuid4()
    Movie.objects.create(
        id=movie_id,
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )

    response = client.get(f"/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["success"] == False

@pytest.mark.django_db
def test_get_movie_by_name(client, db):
    # Create a movie for testing
    Movie.objects.create(
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )

    # Test fetching the movie by its name
    response = client.get("/Test Movie")
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 1  # Expecting one movie in the response
    assert response.json()["response"][0]["name"] == "Test Movie"

@pytest.mark.django_db
def test_get_movie_by_name_not_found(client, db):
    # Create a movie for testing
    Movie.objects.create(
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )

    # Test fetching the movie by its name
    response = client.get("/Test movie")
    assert response.status_code == 404
    assert response.json()["success"] == False

@pytest.mark.django_db
def test_get_movie_by_ranking(client, db):
    # Create a movie for testing
    Movie.objects.create(
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=18
    )

    # Test fetching the movie by its name
    response = client.get(f"/{18}")
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 1  # Expecting one movie in the response
    assert response.json()["response"][0]["name"] == "Test Movie"

@pytest.mark.django_db
def test_get_movie_by_ranking_not_found(client, db):
    # Create a movie for testing
    Movie.objects.create(
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=18
    )

    # Test fetching the movie by its name
    response = client.get(f"/{19}")
    assert response.status_code == 404
    assert response.json()["success"] == False

@pytest.mark.django_db
def test_get_movie_by_date(client, db):
    # Create a movie for testing
    Movie.objects.create(
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )

    # Test fetching the movie by its name
    response = client.get("/2024-03-27")
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 1  # Expecting one movie in the response
    assert response.json()["response"][0]["name"] == "Test Movie"

@pytest.mark.django_db
def test_get_movie_by_date_not_found(client, db):
    # Create a movie for testing
    Movie.objects.create(
        name="Test Movie",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )

    # Test fetching the movie by its name
    response = client.get("/2024-003-27")
    assert response.status_code == 404
    assert response.json()["success"] == False

@pytest.mark.django_db
def test_get_movies(client, db):
    # Create some movies for testing
    Movie.objects.create(
        name="Movie 1",
        protagonists=["Actor 1", "Actor 2"],
        status="running",
        start_date=datetime(2024, 3, 27),
        ranking=8
    )
    Movie.objects.create(
        name="Movie 2",
        protagonists=["Actor 3", "Actor 4"],
        status="starting",
        start_date=datetime(2024, 3, 28),
        ranking=6
    )
    Movie.objects.create(
        name="Movie 3",
        protagonists=["Actor 5", "Actor 6"],
        status="coming-up",
        start_date=datetime(2024, 3, 29),
        ranking=9
    )

    # Test fetching movies sorted by name
    response = client.get("/", params={"sort_by": "name"})
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 3  # Expecting three movies in the response
    assert response.json()["response"][0]["name"] == "Movie 3"

    # Test fetching movies sorted by ranking
    response = client.get("/", params={"sort_by": "ranking"})
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 3  # Expecting three movies in the response
    assert response.json()["response"][0]["ranking"] == 9

    # Test fetching movies sorted by status
    response = client.get("/", params={"sort_by": "status"})
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 3  # Expecting three movies in the response
    assert response.json()["response"][0]["status"] == "coming-up"

    # Test fetching movies sorted by start date
    response = client.get("/", params={"sort_by": "start_date"})
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert len(response.json()["response"]) == 3  # Expecting three movies in the response
    assert response.json()["response"][0]["start_date"] == "2024-03-29"

#update test----

@pytest.mark.django_db
def test_update_movie_success(client, db):
    movie = Movie.objects.create(name="The Old Movie", protagonists=["Alice", "Bob"], status=MovieStatus.coming_up, start_date=datetime(2024, 3, 27), ranking=8)

    response = client.patch(f"/update/{movie.id}")

    assert response.status_code == 200
    assert response.json()['success'] == True

    updated_movie = Movie.objects.get(pk=movie.id)
    assert updated_movie.name == "The Old Movie"
    assert updated_movie.protagonists == ["Alice", "Bob"]
    assert updated_movie.status == MovieStatus.coming_up
    


@pytest.mark.django_db
def test_update_movie_multiple_fields(client, db):
    movie = Movie.objects.create(name="The Old Movie", protagonists=["Alice", "Bob"], status=MovieStatus.starting, start_date=datetime(2024, 3, 27), ranking=8)

    response = client.patch(f"/update/{movie.id}")

    assert response.status_code == 200
    assert response.json()['success'] == True

    updated_movie = Movie.objects.get(pk=movie.id)
    assert updated_movie.name == "The Old Movie"
    assert updated_movie.protagonists == ["Alice", "Bob"]
    assert updated_movie.status == MovieStatus.starting


@pytest.mark.django_db
def test_update_movie_not_found(client, db):

    response = client.patch(f"/update/795c9920-5d51-45a3-9ecb-0b8be7cab97b")  # Invalid ID
    
    assert response.status_code == 404
    assert response.json() == {"success": False, "message": "Movie not found"}

# Optional tests for file uploads (if applicable):

#delete test----
@pytest.mark.django_db
def test_delete_movie_success(client, db):
    # Create a movie for testing
    movie_id = uuid4()
    Movie.objects.create(id=movie_id, name="Test Movie",protagonists=["Actor 5", "Actor 6"],
        status="coming-up",
        start_date=datetime(2024, 3, 29),
        ranking=9
    )
    # Send DELETE request to delete the movie
    response = client.delete(f"/delete/{movie_id}")

    # Assert response status and data
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert Movie.objects.filter(id=movie_id).exists() == False  # Movie should be deleted from the database

@pytest.mark.django_db
def test_delete_movie_not_found(client, db):
    # Send DELETE request with a non-existing movie ID
    movie_id = uuid4()
    response = client.delete(f"/delete/{movie_id}",content_type='application/json')

    # Assert response status and data
    assert response.status_code == 404
    assert response.json()["success"] == False


#celery tests ------------------------------


@pytest.mark.django_db
def test_increase_movie_ranking(db):
    # Create test movies with different statuses
    movie1 = Movie.objects.create(name="Movie 1", protagonists=['hello', 'john'], status="coming-up", start_date=datetime(2024, 3, 27), ranking=50)
    movie2 = Movie.objects.create(name="Movie 2", protagonists=['hello', 'john'], status="starting", start_date=datetime(2024, 3, 27), ranking=75)
    movie3 = Movie.objects.create(name="Movie 3", protagonists=['hello', 'john'], status="running", start_date=datetime(2024, 3, 27), ranking=100)
    movie4 = Movie.objects.create(name="Movie 4", protagonists=['hello', 'john'], status="pending", start_date=datetime(2024, 3, 27), ranking=25)  # Not eligible for ranking increase
    
    # Call the celery task
    task_result = increase_movie_ranking()

    # Assert updated rankings for eligible movies
    movie1.refresh_from_db()
    assert movie1.ranking == 60
    movie2.refresh_from_db()
    assert movie2.ranking == 85
    movie3.refresh_from_db()
    assert movie3.ranking == 110

    # Assert ranking remains unchanged for ineligible movie
    movie4.refresh_from_db()
    assert movie4.ranking == 25
