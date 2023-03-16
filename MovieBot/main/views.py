from django.shortcuts import render
from main.models import Actor, UserSession
from main.populateDB import populate


def populate_database(request):
    (m, g, a)=populate()
    message = 'It has been loaded ' + str(m) + ' movies; ' + str(g) + ' genres; ' + str(a) + ' actors.'
    return render(request, 'base_POPULATEDB.html', {'title': 'End of database load', 'message':message})

def index(request):
    #DELETE ALL UserSession with more than 24 hours since their date_created:
    return render(request, 'base_INDEX.html')