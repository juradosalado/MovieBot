import time
from main.RS import *
from main.models import Actor, Genre
from django.utils import timezone
from django.db.models import Q

def isRelevanceValid(relevance, user_session):
    print("No es valido colega")
    if int(relevance) <=0 or int(relevance) >10:
        response={
            'fulfillmentText': "Oops. Necesito que el número que des esté entre 1 y 10",
            'session': user_session.session_id

        }
        return False, response
    else:
        return True, {}

def usuarioDaNombre(parameters, user_session):
    session_id = user_session.session_id
    reset_scores(user_session)
    #set user_session date_last_used to right now:
    user_session.date_last_used = timezone.now()
    name = parameters['person']['name']
    user_session.name = name
    user_session.is_waiting = False
    user_session.save()
    #dict_parameters['userName'] = name
    text = "Encantado de conocerte, " +name+"! Empezemos con la ronda de preguntas que me ayudarán a encontrarte una buena película para ver. ¿Que genero/s te gustan? Si eres de los que les da igual el género o crees que no es relevante, por favor dime que los géneros no es relevante."
    #print(text)
    response = {
            'fulfillmentText': text,
            'session': session_id
        }
    return response

def usuarioDaGenero(parameters, user_session):
    session_id = user_session.session_id
    genres_list = parameters['generos']
    #Get all genres that contains the names in the list genres:
    genres = Genre.objects.filter(Q(name__in=genres_list))
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.genres.set(genres)
    user_session.save()
    print("User genres: "+str(genres))
    response = {
        'session': user_session.session_id
    }
    
    return response

def usuarioDaGeneroRelevancia(parameters, user_session):
    session_id = user_session.session_id
    relevance = parameters['number-integer']
    isRelValid, response = isRelevanceValid(relevance, user_session)
    if not isRelValid:
        return response
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.genres_relevance = int(relevance)
    user_session.save()
    waiting = user_session.is_waiting
    while(waiting):
        time.sleep(3)
        user_session = UserSession.objects.get(session_id=session_id)
        waiting = user_session.is_waiting
    user_session.is_waiting = True
    user_session.save()
    add_genres_score(user_session)
    dict_ordered = dict(list(sorted(dictScores[user_session].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaPuntuacion(parameters, user_session):
    print("He entrado en usuarioDaPuntuacion")
    session_id = user_session.session_id
    rate = parameters["number"]
    print(rate)
    print("User rate: "+str(rate))
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.rating = float(rate)
    user_session.save()
    print(user_session.rating)
    response = {
        'session': user_session.session_id
    }
    return response


def usuarioDaPuntuacionRelevancia(parameters, user_session):
    session_id = user_session.session_id
    relevance = parameters['number-integer']
    isRelValid, response = isRelevanceValid(relevance, user_session)
    if not isRelValid:
        return response
    waiting = user_session.is_waiting
    while(waiting):
        time.sleep(3)
        user_session = UserSession.objects.get(session_id=session_id)
        waiting = user_session.is_waiting
    user_session.is_waiting = True
    user_session.rating_relevance = int(relevance)
    user_session.save()
    add_ratings_score(user_session)
    dict_ordered = dict(list(sorted(dictScores[user_session].items(), key=lambda item: (-item[1])))[:20])
    #get first film of dict_ordered:
    top_films = list(dict_ordered.keys())[:3]
    
    # Crea una lista de diccionarios con la información de las películas
    movie_data_list = []
    movie_titles = ""

    for film in top_films:
        movie_titles += film.title + ", "
        movie_data = {
            "movie_cover": film.cover_url,
            "movie_title": film.title,
            "movie_synopsis": film.synopsis,
            "movie_rating": film.imdb_rating,
        }
        movie_data_list.append(movie_data)

    # Crea una lista de tarjetas para enviar a Telegram
    telegram_cards = []
    i=1
    for movie_data in movie_data_list:
        card = {
            "card": {
                "title": "#"+str(i)+" "+ movie_data["movie_title"],
                "subtitle": movie_data["movie_synopsis"] + "\nImdb Rating: " + str(movie_data["movie_rating"]),
                "imageUri": movie_data["movie_cover"],
            },
            "platform": "TELEGRAM",
        }
        telegram_cards.append(card)
        i+=1

    response = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": ["Tus recomendaciones son " + movie_titles],
                },
            },
            *telegram_cards,
        ],
    }
    return response

def usuarioDaPais(parameters, user_session):
    session_id = user_session.session_id
    country = parameters["location"]["country"]
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.country = country
    print(user_session.country)
    print(user_session.is_waiting)
    user_session.save()
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaPaisRelevancia(parameters, user_session):
    session_id = user_session.session_id
    relevance = parameters['number-integer']
    isRelValid, response = isRelevanceValid(relevance, user_session)
    if not isRelValid:
        return response
    waiting = user_session.is_waiting
    while(waiting):
        time.sleep(3)
        user_session = UserSession.objects.get(session_id=session_id)
        waiting = user_session.is_waiting
    user_session.is_waiting = True
    user_session.country_relevance = int(relevance)
    user_session.save()
    add_country_score(user_session)
    dict_ordered = dict(list(sorted(dictScores[user_session].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaAnyo(parameters, user_session):
    session_id = user_session.session_id
    years = parameters['number-integer']
    yearAfter = years[0]
    yearBefore = years[1]
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.year_after = int(yearAfter)
    user_session.year_before = int(yearBefore)
    user_session.save()
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaAnyoRelevancia(parameters, user_session):
    session_id = user_session.session_id
    relevance = parameters['number-integer']
    isRelValid, response = isRelevanceValid(relevance, user_session)
    if not isRelValid:
        return response
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.year_relevance = int(relevance)
    user_session.save()
    waiting = user_session.is_waiting
    while(waiting):
        time.sleep(3)
        user_session = UserSession.objects.get(session_id=session_id)
        waiting = user_session.is_waiting
    user_session.is_waiting = True
    user_session.save()
    add_year_score(user_session)
    dict_ordered = dict(list(sorted(dictScores[user_session].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaDuracion(parameters, user_session):
    print("HE ENTRADO")
    session_id = user_session.session_id
    duration = parameters['number-integer']
    print("ESTA ES LA DURACION:", duration)
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.duration = int(duration)
    user_session.save()
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaDuracionRelevancia(parameters, user_session):
    session_id = user_session.session_id
    relevance = parameters['number-integer']
    isRelValid, response = isRelevanceValid(relevance, user_session)
    if not isRelValid:
        return response
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.duration_relevance = int(relevance)
    user_session.save()
    waiting = user_session.is_waiting
    while(waiting):
        time.sleep(3)
        user_session = UserSession.objects.get(session_id=session_id)
        waiting = user_session.is_waiting
    user_session.is_waiting = True
    user_session.save()
    add_duration_score(user_session)
    dict_ordered = dict(list(sorted(dictScores[user_session].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaActores(parameters, user_session):
    session_id = user_session.session_id
    actors_list = parameters['actores']
    #Get all genres that contains the names in the list genres:
    actors = Actor.objects.filter(Q(name__in=actors_list))
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.actors.set(actors)
    user_session.save()
    response = {
        'session': user_session.session_id
    }
    return response

def usuarioDaActoresRelevancia(parameters, user_session):
    session_id = user_session.session_id
    relevance = parameters['number-integer']
    isRelValid, response = isRelevanceValid(relevance, user_session)
    if not isRelValid:
        return response
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.actors_relevance = int(relevance)
    user_session.save()
    waiting = user_session.is_waiting
    while(waiting):
        time.sleep(3)
        user_session = UserSession.objects.get(session_id=session_id)
        waiting = user_session.is_waiting
    user_session.is_waiting = True
    user_session.save()
    add_actors_score(user_session)
    dict_ordered = dict(list(sorted(dictScores[user_session].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))
    response = {
        'session': user_session.session_id
    }
    return response


