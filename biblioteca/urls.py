from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from usuarios import views

urlpatterns = [
    path('', lambda request: redirect('sobre/')),
    # path('', lambda request: redirect('auth/login/')),
    path('admin/', admin.site.urls),
    path('livro/', include('livro.urls')),
    path('auth/', include('usuarios.urls')),
    path('contato/', views.contato_view, name='contato'),
    path('eventos/', views.evento_view, name='eventos'),
    path('galeria/', views.galeria_view, name='galeria'),
    path('login/', views.login_view, name='login'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('index/', views.index_view, name='index'),
    path('deezer/', include('deezer_integration.urls')),
    # path('spotify/', include('spotify_integration.urls')),
]
