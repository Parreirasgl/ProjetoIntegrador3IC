# spotify_integration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('artistas_por_genero/', views.artistas_por_genero, name='artistas_por_genero'),
]
