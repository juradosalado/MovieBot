from django.contrib import admin

# Register your models here.
from .models import Actor, Genre, Movie, UserSession

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(UserSession)

