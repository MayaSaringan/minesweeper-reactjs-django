
from minesweeper_app.models import Game,Storage,Square,Board
import random
import math
import json

def test():
    return "apple"

def getSquare(id,x,y):

    g = Game.objects.get(pk=id)
    if not(g.ongoing): return None
    b =Board.objects.get(game=g)
    s = Square.objects.get(key=(str(id)+":"+str(x)+"-"+str(y)))
    s.hidden=False
    s.save()
    return s.value

def flagSquare(id,x,y):

    g = Game.objects.get(pk=id)
    if not(g.ongoing): return None
    s = Square.objects.get(key=(str(id)+":"+str(x)+"-"+str(y)))
    s.flagged = True
    s.save()
    return None

def isNeighbour(square1,square2):
    if ((square1['x'] + 1 == square2['x'] and square1['y']==square2['y']) or
    (square1['x'] - 1 == square2['x'] and  square1['y']==square2['y']) or
    (square1['x'] + 1 == square2['x'] and square1['y']+1==square2['y']) or
    (square1['x'] + 1 == square2['x'] and  square1['y']-1==square2['y']) or
    (square1['x'] - 1 == square2['x'] and  square1['y']+1==square2['y']) or
    (square1['x'] - 1 == square2['x'] and  square1['y']-1==square2['y']) or
    (square1['x'] == square2['x'] and  square1['y']+1==square2['y']) or
    (square1['x'] == square2['x'] and  square1['y']-1==square2['y'])):
        return True
    return False

def expandNeighbours(id,x,y):
    try:
        g = Game.objects.get(pk=id)
        b =Board.objects.get(game=g)
        allSquares = Square.objects.filter(board=b)
        originSquare = Square.objects.get(key=(str(id)+":"+str(x)+"-"+str(y)))
        uncovered = []
        uncovered.append({'x':originSquare.xcoord,'y':originSquare.ycoord,'value':originSquare.value})
        s = list(filter(lambda item:item.value==0,allSquares))
        for item in s:
            for otherItem in uncovered:
                itemC = {'x':item.xcoord,'y':item.ycoord,'value':item.value}

                if isNeighbour(itemC,otherItem) and not(itemC in uncovered):
                    uncovered.append(itemC)

        s2 = list(filter(lambda item:item.value!=0,allSquares))
        for item in s2:
            for otherItem in uncovered:
                itemC = {'x':item.xcoord,'y':item.ycoord,'value':item.value}

                if otherItem['value'] ==0 and isNeighbour(itemC,otherItem):
                    if  not(itemC in uncovered):
                        uncovered.append(itemC)
        #print(uncovered)
        #get all cells bordering the empty tiles
        return uncovered
    except Game.DoesNotExist:
        return None

def createGame():
    numGames = Storage.objects.get(id=0).numGames
    size=6
    g = Game.objects.create(id=(numGames),storage =Storage.objects.get(id=0))
    b = Board.objects.create(game=g,size=6)
    board = []
    bombLocs = random.sample(range(size*size),math.floor((1/6)*(size*size)))
    counter =0
    for x in range(6):
        row = []
        for y in range(6):

            if (counter in bombLocs):
                Square.objects.create(
                    value=1000,
                    board=b,
                    key=(str(numGames)+":"+str(x)+"-"+str(y)),
                    hidden=True,
                    xcoord=x,
                    ycoord=y)
            else:
                bombsNearby =0
                if ((counter-1) in bombLocs) and (y-1)>=0 and (y-1)<size:
                    bombsNearby = bombsNearby+1
                if (counter-size-1) in bombLocs and (y-1)  >=0 and (y-1) <size and (x-1)  >=0 and (x-1) <size:
                    bombsNearby = bombsNearby+1
                if (counter-size) in bombLocs and (x-1)  >=0 and (x-1) <size:
                    bombsNearby = bombsNearby+1
                if (counter-size+1) in bombLocs and (x-1)  >=0 and (x-1) <size and (y+1)  >=0 and (y+1)<size :
                    bombsNearby = bombsNearby+1
                if (counter+1) in bombLocs and (y+1)  >=0 and (y+1) :
                    bombsNearby = bombsNearby+1
                if (counter+size+1) in bombLocs and (x+1)  >=0 and (x+1) <size and (y+1)  >=0 and (y+1) <size:
                    bombsNearby = bombsNearby+1
                if (counter+size) in bombLocs and (x+1)  >=0 and (x+1) <size:
                    bombsNearby = bombsNearby+1
                if (counter+size-1) in bombLocs and (x+1)  >=0 and (x+1) <size and (y-1)>=0 and (y-1)<size:
                    bombsNearby = bombsNearby+1
                Square.objects.create(value=bombsNearby,board=b,key=(str(numGames)+":"+str(x)+"-"+str(y)),hidden=True,xcoord=x,
                ycoord=y)


            row.append(None)
            counter+=1
        board.append(row)
    numGames = numGames+1
    s =Storage.objects.get(id=0)
    s.numGames =numGames
    s.save()
    return {'id':numGames-1,'board':board,'size':6}

def retrieveGame(id):
    #fetch game from database if it exists
    #excpted to return id, board and size
    numGames = -1
    try:
        g = Game.objects.get(pk=id)
        board = []
        b =Board.objects.get(game=g)
        size = b.size
        allSquares = Square.objects.filter(board=b)

        for y in range(size):
            row = []
            for x in range(size):
                s = list(filter(lambda item:item.key==(str(id)+":"+str(x)+"-"+str(y)),allSquares))

                if (s[0].hidden):
                    row.append(None)
                else:
                    row.append(s[0].value)
            board.append(row)

        #retreive Board}
        return {'id':id,'board':board,'size':size}
        #return "got id at "+str(id)
    except Game.DoesNotExist:
        return None


    #Game.objects.create(id=Storage.objects.get())
    #otherwise create it

    #return ("stub"+str(Storage.objects.get(id=0).numGames))

def emptyDB():
    Game.objects.all().delete()
    Board.objects.all().delete()
    Square.objects.all().delete()
    s =Storage.objects.get(id=0)

    s.numGames =0
    s.save()

def getBombLocs(id):
    try:
        g = Game.objects.get(pk=id)
        bombs=[]
        g.ongoing = False
        g.save()
        b =Board.objects.get(game=g)
        size = b.size
        allSquares = Square.objects.filter(board=b)
        s = list(filter(lambda item:item.value==1000,allSquares))
        for item in s:
            bombs.append({'x':item.xcoord,'y':item.ycoord})
            item.hidden=False
            item.save()



        #retreive Board}
        return bombs
        #return "got id at "+str(id)
    except Game.DoesNotExist:
        return None
