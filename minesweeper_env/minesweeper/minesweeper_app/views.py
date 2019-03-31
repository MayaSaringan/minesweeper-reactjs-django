
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from . import logic
def menu(request):
    template = loader.get_template('public/menu.html')
    return render(request,'public/menu.html')

def getSession(request,gameID):
    template = loader.get_template('public/index.html')
    gameDetails = logic.retrieveGame(gameID)

    #return JsonResponse()
    return render(request,'public/index.html',{'id':gameDetails['id'],'board':gameDetails['board'],'size':gameDetails['size']})

def square(request,gameID):
    #take url requests like ---gameID/square?x=#&y=#
    x = request.GET['x']
    y =request.GET['y']
    #return HttpResponse("requested information for square at x "+x +" and y "+y)
    return JsonResponse({'value':logic.getSquare(gameID,x,y)})

def game(request,gameID):
    gameDetails = logic.retrieveGame(gameID)
    if gameDetails is None:
        return JsonResponse({'id':None})

    return JsonResponse({'id':gameDetails['id'],'board':gameDetails['board'],'size':gameDetails['size']})

def create(request):
    gameDetails = logic.createGame()
    return HttpResponseRedirect('/session/'+str(gameDetails['id'])+"/")
    #return JsonResponse({'id':gameDetails['id'],'board':gameDetails['board'],'size':gameDetails['size']})



def emptyDB(request):
    logic.emptyDB()
    return HttpResponse("Emptied DB")

def lost(request,gameID):
    bombLocs  = logic.getBombLocs(gameID)
    return JsonResponse(bombLocs,safe=False)

def squareExpand(request,gameID):
    #take url requests like ---gameID/square?x=#&y=#
    x = request.GET['x']
    y =request.GET['y']
    squares = logic.expandNeighbours(gameID,x,y)
    #return HttpResponse("requested information for square at x "+x +" and y "+y)
    return JsonResponse(squares,safe=False)

def favicon(request):
    return
