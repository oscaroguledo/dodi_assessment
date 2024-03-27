from django.test import TestCase


import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import Movie

# Create your tests here.
@pytest.mark.django_db
def test_movie_creation():
    # Create a Movie instance
    movie = Movie.objects.create(
        name='Test Movie',
        protagonists=['Protagonist 1', 'Protagonist 2'],
        poster=SimpleUploadedFile('poster.jpg', b'content', content_type='image/jpeg'),
        trailer=SimpleUploadedFile('trailer.mp4', b'content', content_type='video/mp4'),
        start_date='2022-01-01',
        status='coming_up',
        ranking=0
    )
    
    # Verify that the movie object is created successfully
    assert movie.id is not None
    assert movie.name == 'Test Movie'
    assert movie.protagonists == ['Protagonist 1', 'Protagonist 2']
    assert movie.poster.name == 'posters/poster.jpg'
    assert movie.trailer.name == 'trailers/trailer.mp4'
    assert movie.start_date == '2022-01-01'
    assert movie.status == 'coming_up'
    assert movie.ranking == 0

@pytest.mark.django_db
def test_movie_str_representation():
    # Create a Movie instance
    movie = Movie.objects.create(
        name='Test Movie',
        protagonists=['Protagonist 1', 'Protagonist 2'],
        poster=SimpleUploadedFile('poster.jpg', b'content', content_type='image/jpeg'),
        trailer=SimpleUploadedFile('trailer.mp4', b'content', content_type='video/mp4'),
        start_date='2022-01-01',
        status='coming_up',
        ranking=0
    )
    
    # Verify the __str__() method of the Movie model
    assert str(movie) == 'Test Movie'
