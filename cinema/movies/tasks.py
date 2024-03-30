from celery import shared_task


@shared_task()
def increase_movie_ranking():
    print("Increasing movie ranking...")
    from .models import Movie, models
    
    movies = Movie.objects.filter(models.Q(status="coming-up") | models.Q(status="starting")| models.Q(status="running"))
    for movie in movies:
        movie.ranking += 10
        movie.save()
    return 'done'
