from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('session/<int:gameID>/',views.getSession,name='getSession'),
    path('<int:gameID>/square',views.square,name="squareVal"),
    path('<int:gameID>/',views.game,name="game"),
    path('emptyDB/',views.emptyDB,name="emptyDB"),
    path('create/',views.create,name="create"),
    path('<int:gameID>/lost/',views.lost,name="lost"),
    path('<int:gameID>/expand/square',views.squareExpand,name="squareExpand"),
    path('favicon.ico/',views.favicon,name="favicon"),
]
