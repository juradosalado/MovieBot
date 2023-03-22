import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render
from main.models import Actor, UserSession
from main.populateDB import populate
from main.RS import *
from datetime import datetime, timedelta
from .fulfillments import *

from django.views.decorators.csrf import csrf_exempt

def deleteOldUserSessions():
    OldUserSessions= UserSession.objects.filter(date_last_used__lt=datetime.now()-timedelta(days=1))
    for oldusersession in OldUserSessions:
        if oldusersession in dictScores:
            del dictScores[oldusersession]
        if oldusersession.session_id in dictMatching:
            del dictMatching[oldusersession]
    OldUserSessions.delete()

def populate_database(request):
    (m, g, a)=populate()
    message = 'It has been loaded ' + str(m) + ' movies; ' + str(g) + ' genres; ' + str(a) + ' actors.'
    return render(request, 'base_POPULATEDB.html', {'title': 'End of database load', 'message':message})

def index(request):
    deleteOldUserSessions()
    return render(request, 'base_INDEX.html')

@csrf_exempt
def webhook(request):
    print("Empeizan prints")
    print(request.session)
    # Get the session ID from the request
    req = json.loads(request.body)
    if 'session' in req:
        session_id = req['session']
        print("Esta es la id:"+ session_id)
    else:
        session_id = str(uuid.uuid4())
        print("Esta es la nueva id:"+ session_id)
    
    #Get User_Session by session_id and create one if it doesnt exist:
    user_session = UserSession.objects.filter(session_id=session_id)
    if not user_session:
        user_session = UserSession.objects.create(session_id=session_id)
        user_session.save()
    else:
        user_session = user_session[0]
    print("EL USER SESSION ES:"+str(user_session))


    intent = req['queryResult']['intent']['displayName']
    #get the entities from the request:
    parameters = req['queryResult']['parameters']
    #get the age:
    print(parameters)
    response= {
        
    }
    if intent == 'UsuarioDaNombre':
        response = usuarioDaNombre(parameters, user_session)
    elif intent == 'UsuarioDaGenero':
        response = usuarioDaGenero(parameters, user_session)
    elif intent == 'UsuarioDaGeneroRelevancia':
        response = usuarioDaGeneroRelevancia(parameters, user_session)
    elif intent == 'UsuarioDaActores':
        response = usuarioDaActores(parameters, user_session)
    elif intent == 'UsuarioDaActoresRelevancia':
        response = usuarioDaActoresRelevancia(parameters, user_session)
    elif intent == 'UsuarioDaPais':
        response = usuarioDaPais(parameters, user_session)
    elif intent == 'UsuarioDaPaisRelevancia':
        response = usuarioDaPaisRelevancia(parameters, user_session)
    elif intent == 'UsuarioDaDuración':
        response = usuarioDaDuracion(parameters, user_session)
    elif intent == 'UsuarioDaDuracionRelevancia':
        response = usuarioDaDuracionRelevancia(parameters, user_session)
    elif intent == 'UsuarioDaAnyo':
        response = usuarioDaAnyo(parameters, user_session)
    elif intent == 'UsuarioDaAnyoRelevancia':
        response = usuarioDaAnyoRelevancia(parameters, user_session)
    elif intent == 'UsuarioDaPuntuacion':
        response = usuarioDaPuntuacion(parameters, user_session)
    elif intent == 'UsuarioDaPuntuacionRelevancia':
        response = usuarioDaPuntuacionRelevancia(parameters, user_session)
    return JsonResponse(response)