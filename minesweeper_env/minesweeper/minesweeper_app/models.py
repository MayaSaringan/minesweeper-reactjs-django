from django.db import models

# Create your models here.

class Storage(models.Model):
    #has games
    numGames = models.IntegerField(default=0)
    id= models.IntegerField(default=0,primary_key=True)

    def __str__(self):
        return "ass"+str(self.id);

class Game(models.Model):
    #has a Board
    ongoing = models.BooleanField(default=True)
    storage = models.ForeignKey(Storage,on_delete=models.CASCADE)
    id= models.CharField(max_length=200,primary_key=True)

class Board(models.Model):
    #has squares
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    size =models.IntegerField(default=0)

class Square(models.Model):
    value = models.IntegerField(default=0)
    xcoord = models.IntegerField(default=0)
    ycoord = models.IntegerField(default=0)
    board=models.ForeignKey(Board,on_delete=models.CASCADE)
    key = models.CharField(max_length=200,default="notassigned",null=False,primary_key=True)
    hidden = models.BooleanField(default=True)
