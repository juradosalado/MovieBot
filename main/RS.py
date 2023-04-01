from main.models import Movie, UserSession


movies = Movie.objects.all()
dictScores = dict()
dictMatching = dict()

def reset_scores(user_session):
    if user_session in dictScores:
        dictScores[user_session].clear()
    if user_session in dictMatching:
        dictMatching[user_session].clear()


def add_year_score(user_session):
    session_id = user_session.session_id
    year_before = user_session.year_before
    year_after = user_session.year_after
    year_relevance = user_session.year_relevance
    for movie in movies:
        if movie.year is not None:
            if movie.year >= year_after:
                if movie.year <= year_before:
                    if user_session in dictScores:
                        if movie in dictScores[user_session]:
                            dictScores[user_session][movie] += year_relevance
                        else:
                            dictScores[user_session][movie] = year_relevance
                    else:
                        dictScores[user_session] = {movie: year_relevance}
                    
                else:
                    if user_session in dictScores:
                        if movie in dictScores[user_session]:
                            #Se eliminará la misma cantidad que la relevancia introducida si una peli se estrenó 10 años antes o después del rango
                            dictScores[user_session][movie] -= (movie.year - year_before) * year_relevance / 10
                        else:
                            dictScores[user_session][movie] = -(movie.year - year_before) * year_relevance / 10
                    else:
                        dictScores[user_session] = dict()
                        dictScores[user_session][movie] = -(movie.year - year_before) * year_relevance / 10
            else:
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        dictScores[user_session][movie] -= (year_after - movie.year) * year_relevance / 10
                    else:
                        dictScores[user_session][movie] = -(year_after - movie.year) * year_relevance / 10
                else:
                    dictScores[user_session] = dict()
                    dictScores[user_session][movie] = -(year_after - movie.year) * year_relevance / 10
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.is_waiting = False
    user_session.save()

def add_duration_score(user_session):
    session_id = user_session.session_id
    duration = user_session.duration
    print(duration)
    duration_relevance = user_session.duration_relevance
    for movie in movies:
        if movie.duration is not None:
            if movie.duration <= int(duration):
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        dictScores[user_session][movie] += duration_relevance
                    else:
                        dictScores[user_session][movie] = duration_relevance
                else:
                    dictScores[user_session] = {movie: duration_relevance}
            else:
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        #Se eliminará la relevancia si una peli dura 45 minutos más
                        dictScores[user_session][movie] -= (movie.duration -duration) * duration_relevance / 45
                    else:
                        dictScores[user_session][movie] = -(movie.duration-duration) * duration_relevance / 45
                else:
                    dictScores[user_session] = dict()
                    dictScores[user_session][movie] = (movie.duration-duration) * duration_relevance / 45
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.is_waiting = False
    user_session.save()

def add_actors_score(user_session):
    session_id = user_session.session_id
    actors = user_session.actors.all()
    actors_relevance = user_session.actors_relevance
    for movie in movies:
        for actor in actors:
            if actor in movie.actors.all():
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        dictScores[user_session][movie] += actors_relevance / len(actors)
                    else:
                        dictScores[user_session][movie] = actors_relevance / len(actors)
                else:
                    dictScores[user_session] = {movie: actors_relevance}
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.is_waiting = False
    user_session.save()

def add_genres_score(user_session):
    session_id = user_session.session_id
    genres = user_session.genres.all()
    genres_relevance = user_session.genres_relevance
    for movie in movies:
        for genre in genres:
            if genre in movie.genres.all():
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        dictScores[user_session][movie] += genres_relevance / len(genres)
                    else:
                        dictScores[user_session][movie] = genres_relevance / len(genres)
                else:
                    dictScores[user_session] = {movie: genres_relevance / len(genres)}
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.is_waiting = False
    user_session.save()

def add_ratings_score(user_session):
    session_id = user_session.session_id
    rating = user_session.rating
    rating_relevance = user_session.rating_relevance
    for movie in movies:
        if movie.imdb_rating is not None:
            if movie.imdb_rating >= rating:
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        dictScores[user_session][movie] += rating_relevance
                    else:
                        dictScores[user_session][movie] = rating_relevance
                else:
                    dictScores[user_session] = {movie: rating_relevance}
            else:
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        #Quita la relevancia si la nota es inferior en dos puntos
                        dictScores[user_session][movie] -= (rating - float(movie.imdb_rating)) * rating_relevance / 2
                    else:
                        dictScores[user_session][movie] = -(rating - float(movie.imdb_rating)) * rating_relevance / 2
                else:
                    dictScores[user_session] = dict()
                    dictScores[user_session][movie] = -(rating - float(movie.imdb_rating)) * rating_relevance / 2
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.is_waiting = False
    user_session.save()

def add_country_score(user_session):
    session_id = user_session.session_id
    country = user_session.country
    country_relevance = user_session.country_relevance
    for movie in movies:
        if movie.country is not None:
            if country in movie.country:
                if user_session in dictScores:
                    if movie in dictScores[user_session]:
                        dictScores[user_session][movie] += country_relevance
                    else:
                        dictScores[user_session][movie] = country_relevance
                else:
                    dictScores[user_session] = {movie: country_relevance}
    user_session = UserSession.objects.get(session_id=session_id)
    user_session.is_waiting = False
    user_session.save()