from django.shortcuts import render
from main.models import Actor, UserSession
from main.populateDB import populate
from main.RS import *


def populate_database(request):
    (m, g, a)=populate()
    message = 'It has been loaded ' + str(m) + ' movies; ' + str(g) + ' genres; ' + str(a) + ' actors.'
    return render(request, 'base_POPULATEDB.html', {'title': 'End of database load', 'message':message})

def index(request):
    #DELETE ALL UserSession with more than 24 hours since their date_created:
    user = UserSession.objects.get(session_id="1")
    reset_scores(user)
    add_year_score(user)
    add_duration_score(user)
    add_actors_score(user)
    add_genres_score(user)
    add_ratings_score(user)
    add_country_score(user)
    dict_ordered = dict(list(sorted(dictScores[user].items(), key=lambda item: (-item[1])))[:20])
    print(str(dict_ordered))
    return render(request, 'base_INDEX.html')