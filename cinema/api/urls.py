from django.urls import path
from .views import *

urlpatterns = [
    # job portal-------------------------------------------
    path("", appStatus.as_view()),
    path("movies", MovieAPIView.as_view()),
]