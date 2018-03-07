from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
import datetime
from django.core import serializers
from .models import Details
from .models import RegistrationsAndParticipations
from django.db.models import F
from itertools import chain
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
#-----------------------------------------------------------------------------------------------------------------------------------------
#EVENT-IDS


#AWD  -  A WALK IN THE DARK
#AER  -  AEROPLANE CHESS
#ALP    -  ALPATCHINO
#ANW  -  ANWEHSA
#BYC  -  BEYCODE
#CHL - CHALLENGICA
#CRC  - CRIMINAL CASE
#CRP  -  CRYPTOTHON
#DXT  - DEXTRA
#KOT  -  KNOCK OFF TOURNAMENT
#TTX  - TECHTRIX

#-----------------------------------------------------------------------------------------------------------------------------------------
#Results Fetch

#Use this function to get end results, Need to modify based upon various filters
@csrf_exempt
def showDetails(request):
    if request.method == 'POST':
        queryset = Details.objects.filter(eId = request.POST.get('eId'))
        json_data = serializers.serialize('json',queryset)
        return HttpResponse(json_data, content_type = "json/application")


@csrf_exempt
def showRegistrationsAndParticipations(request):
    queryset = RegistrationsAndParticipations.objects.all().order_by('pk')
    json_data = serializers.serialize('json',queryset)
    return HttpResponse(json_data, content_type = "json/application")

def showEvent(request):
    queryset = Event.object.all.order_by('pk')
    json_data = serializers.serialize('json',queryset)
    return HttpResponse(json_data, content_type = "json/application")

#----------------------------------------------------------------------------------------------------------------------
# Event App

#Takes Existing Gid and adds Players
# URL @ events/addplayer  
@csrf_exempt
def appendPlayers(request):
    message = 'Err '
    if request.method == 'POST':
        qID = request.post.get('qId').split(',')
        gID = request.post.get('gId')
        # Got data
        queryset = Details.objects.filter(gId = gID)
        #If this game even exists
        if queryset:
            #Check for list of qID's are valid or not
            for s in qID:
                if not validate(queryset.eID,s):
                    user = Profile.objects.get(qId = qID)
                    json_data = sorted(chain(user, queryset))
                    #json_data = user | obj
                    json_data = serializers.serialize('json',user)
                    return HttpResponse(user, content_type = "json/application")
                    message.append(s)
                    #return HttpResponse(message, content_type = "text/plain")
            
            # Append qID ( list ) to queryset
                else:
                    queryset.QId.append(s)

            queryset.status = 'Running'
            queryset.save()
            message = 'Success'
            #Anthe I guess
    else:
        message = 'Invalid Request'
    
    return HttpResponse(message, content_type = "text/plain")
            


#Ends the game adding score and updating participated
# URL events/endgame
@csrf_exempt
def endGame(request):
    message = 'Err'
    if request.method == 'POST':
        GID =  request.POST.get('gId')
        score = request.POST.get('Total')
        #fetch the row with give gId
        queryset = Details.objects.get(gId = GID)
        #update status and score
        queryset.update(status = 'Played',Total = score)
        #append to participated list
        EID = queryset.eId
        list = queryset.QId
        for q in list:
            c = RegistrationsAndParticipations.object.get(QId = q)
            c.participated.append(EID)
            c.save()
    
        queryset.save()
        message = 'Done'
        pass
    else:
        message = 'Invalid Request'
        pass
    return HttpResponse(message, content_type = "text/plain")

#Generates unique GID which doesn't occur in the data base
@csrf_exempt
def generateGID(eID):
    game = Event.objects.get(eId = eID)
    game.eCount = F('eCount')+1
    game.save()
    return "%s%s" %(eID,game.eCount)


#Creates a New Game with a single Qid
# URL events/newgame
@csrf_exempt
def newGame(request):
    message = 'Err'
    if request.method == 'POST':
        eID = request.post.get('eId')
        qID = request.post.get('qId')
        #Collected Required Data
        #Checking for valid QID for this game
        if validateGame(qId,eId):
            #Generating New Game ID
            gID = generateGID(eID)
            #Creating New Row
            obj = Details( eId = eID, qId = qID, Total = 0, gId = gID, status = 'Waiting' )
            obj.save()
            #commiting the row 
            message = 'Success'
            user = Profile.objects.get(qId = qID)
            json_data = sorted(chain(user, obj))
            #json_data = user | obj
            json_data = serializers.serialize('json',user)
            return HttpResponse(user, content_type = "json/application")
        else:
            message = 'Not Applicable'
    else:
        message = 'Not a Valid Request'

    return HttpResponse(message, content_type = "text/plain")
        
    
    

#Authenticates user to the game
#Checks if the user is playing for the first time or not! ^.^
@csrf_exempt
def validateGame(eId,qID):
    flag = False
    #Get the row in this model for the corresponding user
    check = RegistrationsAndParticipations.objects.get(qId = qID)

    #Check if user elgible ie. paid and not participated and registered
    if eId in check.paid and eId in check.registered:
        if eID not in check.participated:
            flag = True

    return flag

#------------------------------------------------------------------------------------------------------------------------------------------------
#Registrations

# URL register/fetch
@csrf_exempt
def getUserEvent(request):
    message = 'Err'
    if request.method == 'POST':
        # Fetch Registrations and participations for paid registered and participated
        query = RegistrationsAndParticipations.objects.filter( qId = request.post.get('qId'))

        #Need to remove participated column
        
        json_data = serializers.serialize('json',query)
        return HttpResponse(json_data,content_type = "json/application")
    else:
        return HttpResponse(message , content_type = "text/plain")

#Replace 
# URL register/push
@csrf_exempt
def modifyRegistrationsAndParticipations(request):
    message = 'Err'
    if request.method == 'POST':
        queryset = RegistrationsAndParticipations.objects.filter( qId = request.post.get('qId'))
        #Fetch request Data
        #pariticapted = request.post.get('participated')
        registered = request.post.get('registered')
        paid = request.post.get('paid')
        #look and replace the fields
        #Removing Current Data
        queryset.paid = []
        queryset.registered = []
        #Adding new data
        #queryset.paid = paid
        #queryset.registered = registered
               
        
        for s in paid:
            queryset.paid.append(s)  
        for s in registered:
            queryset.registered.append(s)
        
        #all operations done
        queryset.save()

        message = 'Success' 

    else:
        message ='Invalid Request'

    return HttpResponse(message, content_type = "text/plain")
        



#---------------------------------------------------------------------------------------------------------------------------------------------------
#This is your code , appending the written code into templates can help us sort it out
# def add_participant(request):
#     if request.method == 'POST':
#         queryset = RegistrationsAndParticipations.objects.all().get(Qid = request.POST.get('QId'))
#         if queryset:
#             if request.POST.get('eId') in queryset.paid:
#                 if request.POST.get('eId') in queryset.participated:
#                     #return render(request,'',{'error_message' = error_message})
#                 else:
#                     gameId = get_random_string(length = 5)
#                     dup_game = Details.objects.get(gId = get_random_string(length = 5))
#                     if dup_game:
#                         return render(request,'',{'error_message' = error_message})
#                     else:
#                         nEvent = Details(status = "Running", eId = request.POST.get('eId'), gId = gameId, QId = request.POST.get('QId'), Total = 0)
#                         nEvent.save()
#                         json_data = serializers.serialize('json',nEvent)
#                         return HttpResponse(json_data, content_type = "application/json")
#             else:
#                 return render(request,'',{'error_message' = error_message})
#     else:
#         return render(request,'',{'error_message' = error_message})
#         # json_data = serializers.serialize('json', queryset)
#         # return HttpResponse(json_data, content_type = "application/json")

# #This will be final request, where 
# def add_scores(request):
#     if request.method = 'POST':
#         queryset1 = Details.objects.filter(gId = request.POST.get('gId')).update(status = "Played", Total = request.POST.get('Total'))
#         queryset2 = RegistrationsAndParticipations.objects.filter(QId = queryset1.QId)
#         for obj in queryset2:
#             obj.participated.append(queryset1.eId)
#             obj.save()
#         json_data = serializers.serialize('json', queryset2)
#         return HttpResponse(json_data, content_type = "application/json")
























# def register(request):
#     if request.method = 'POST':
#         queryset = Profile.objects.get(QId = request.POST.get('QId'))
#         if queryset:
#             queryset1 = RegistrationsAndParticipations.objects.get(QId = queryset.QId)
#             Event = request.POST.get('eId')
#             queryset1.paid.append(Event)
#             json_data = serializers.serialize('json', queryset1)
#             return HttpResponse(json_data, content_type = "application/json")
        
#         # else:
        
#         # 	Profile.objects.create()
#         # 	q1 = Profile.objects.get(QId)
#         # 	Event = request.POST.eId
#         # 	e1 = RegistrationsAndParticipations.objects.get(QId = q1.QId)
#         # 	e1.paid.append(Event)
        
#         else:
#             #messages.error(request, 'ERR
#             return render(request,'',{'error_message' = error_message})a




 
