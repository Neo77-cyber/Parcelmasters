from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name = 'home' ),
    path('track/', views.search, name ='search'),
    path('shipwithus/', views.shipwithus, name = 'shipwithus'),
    path('register', views.register, name = 'register'),
    path('signin/', views.signin, name = 'signin')
]