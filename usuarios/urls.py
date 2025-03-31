from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('validar_cadastro/', views.valida_cadastro, name = 'valida_cadastro'),
    path('validar_login/', views.validar_login, name = 'validar_login'),
    path('sair/', views.sair, name = 'sair'),
    #path('banda_sinfonica/', views.novo_projeto_view, name='banda_sinfonica'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('evento/', views.evento_view, name='evento'),
    path('galeria/', views.galeria_view, name='galeria'),
    path('contato/', views.contato_view, name='contato'),
    
]