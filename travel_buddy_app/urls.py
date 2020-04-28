from django.urls import path     
from . import views
urlpatterns = [
    path('main', views.index),
    path('register', views.register),
    path('travels', views.travels),
    path('logout', views.logout),
    path('login', views.login), 
    path('travels/add', views.addTripForm),
    path('addtrip', views.createTrip),
    path('travels/destination/<tripid>', views.viewDest),
    path('addtraveler/<tripid>', views.addTraveler),
]