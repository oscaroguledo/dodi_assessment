from django.db import models
import uuid
# Create your models here.

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    protagonists = models.JSONField()
    poster=models.ImageField(upload_to='posters/')
    trailer = models.FileField(upload_to='trailers/')
    start_date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=255)
    ranking = models.IntegerField(default=0, null=True)  

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ='movie'
        ordering = ['-ranking','-start_date','name']
