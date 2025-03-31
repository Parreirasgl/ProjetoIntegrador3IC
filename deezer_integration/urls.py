# deezer_integration/urls.py

from django.urls import path
from . import views

app_name = 'deezer_integration'

urlpatterns = [
    path('artistas-por-genero/', views.artistas_por_genero, name='artistas_por_genero'),
]
