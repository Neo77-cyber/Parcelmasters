from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name = 'home' ),
    path('track/', views.track, name ='track'),
    path('shipwithus/', views.newshipping, name = 'shipwithus')
]