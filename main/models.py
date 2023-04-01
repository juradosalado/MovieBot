from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Actor(models.Model):
    name = models.CharField(max_length=255)
    
class Genre(models.Model):
    name = models.CharField(max_length=255)
class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField(validators=[MinValueValidator(1888), MaxValueValidator(2030)])
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)],null=True)
    country = models.CharField(max_length=255)
    synopsis = models.TextField()
    imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],null=True
    )
    cover_url = models.URLField(max_length=255,)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title

class UserSession(models.Model):
    session_id = models.CharField(max_length=320, primary_key=True)
    name = models.TextField(null=True)
    date_last_used = models.DateTimeField(default=timezone.now,null=True)
    is_waiting = models.BooleanField(default=False)
    year_before = models.IntegerField(null=True)
    year_after = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    country = models.CharField(max_length=255, null=True)
    year_relevance = models.IntegerField(null=True)
    duration_relevance = models.IntegerField(null=True)
    country_relevance = models.IntegerField(null=True)
    actors_relevance = models.IntegerField(null=True)
    genres_relevance = models.IntegerField(null=True)
    rating_relevance = models.IntegerField(null=True)
    genres = models.ManyToManyField(Genre,null=True)
    actors = models.ManyToManyField(Actor, null=True)
   
    