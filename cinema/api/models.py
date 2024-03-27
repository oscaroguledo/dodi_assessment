from django.db import models
import jsonfield
# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    protagonists = jsonfield.JSONField()
    poster=models.ImageField(upload_to='posters/')
    trailer = models.FileField(upload_to='trailers/')
    start_date = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    ranking = models.IntegerField(default=0)  

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ='movies'
        ordering = ['ranking']
    
