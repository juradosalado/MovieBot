import ast
import csv
from datetime import datetime
import re
from main.models import Actor,Movie,Genre

def populate():
    (m, g, a)=populate_movies()
    return (m, g, a)

def add_many_to_many(item_id, list_of_items, items_set, cls):
    items = []
    for item in list_of_items:
        if item.strip() not in items_set:
            items_set.add(item.strip())
            itemToAdd=cls(item_id, item.strip())
            itemToAdd.save()
            item_id +=1
        else:
            print(item.strip())
            itemToAdd=cls.objects.filter(name=item.strip()).first()
        items.append(itemToAdd)
    return items, item_id


def populate_movies():
    Movie.objects.all().delete()
    Genre.objects.all().delete()
    Actor.objects.all().delete()

    genres_set = set()
    genre_id = 0

    actors_set = set()
    actor_id = 0
    #título,título_original,año,duración,país,dirección,guion,reparto,productora,género,
    #sinopsis,premios,
    #puntuación_fa,votos_fa,
    #puntuación_positiva,puntuación_neutral,puntuación_negativa,portada_url,portada_local,puntuación_imdb,votos_imdb
    try:
        with open("data\\movies.csv", 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                title = row[1].strip()
                year = row[3].strip()
                duration = row[4].strip()
                if duration == '':
                    duration = None
                else:
                    duration = duration.split()[0]
                country = row[5].strip()
                synopsis = row[11].strip()
                imdb_rating = row[20].strip()
                if imdb_rating == '':
                    imdb_rating = None
                else:
                    imdb_rating = float(imdb_rating)
                cover_url = row[18].strip()
                
                movie=Movie(title=title, year=year, duration=duration, country=country, synopsis=synopsis, imdb_rating=imdb_rating, cover_url=cover_url)
                movie.save()

                list_of_actors = row[8].strip().split(',')
                list_of_actors = [re.sub(r"\(.*?\)", "", a.strip()) for a in list_of_actors]
                actors, actor_id = add_many_to_many(actor_id, list_of_actors, actors_set, Actor)
                movie.actors.set(actors)

                list_of_genres = row[10].strip().split('.')
                genres, genre_id = add_many_to_many(genre_id, list_of_genres, genres_set, Genre)
                movie.genres.set(genres)

                movie.save()
        return (Movie.objects.count(), Genre.objects.count(), Actor.objects.count())

    except FileNotFoundError:
        print("File does not exist")
        return (0,0,0)
