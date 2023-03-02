from django.urls import path 
from . import views


urlpatterns = [
    path('', views.home, name = 'home' ),
    path('track/', views.search, name ='search'),
    path('shipwithus/', views.newshipping, name = 'shipwithus')
]