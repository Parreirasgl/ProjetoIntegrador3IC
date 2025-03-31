import requests
from django.shortcuts import render
from livro.models import Livros
from django.db.models import Count

# URL base da API do Deezer
DEEZER_GENRE_URL = "https://api.deezer.com/genre"

def artistas_por_genero(request):
    # Obtém a lista de gêneros do Deezer
    response = requests.get(DEEZER_GENRE_URL)
    generos_dict = {}

    if response.status_code == 200:
        generos = response.json()["data"]
        generos_dict = {str(g['id']): g['name'].lower() for g in generos}
    else:
        generos = []

    # Inicializa listas vazias
    faixas = []  # Faixas mais populares
    artistas = []  # Artistas mais populares
    livros = Livros.objects.all()

    # Contagem de livros por gênero
    livros_por_genero = Livros.objects.values('genero').annotate(count=Count('id')).order_by('genero')

    # Verifica se o formulário foi enviado
    genre_id = 'todos'  # Inicializa com 'todos' para carregar os dados de "Todos" no início

    if request.method == 'POST':
        genre_id = request.POST['genero']  # ID do gênero selecionado

    if genre_id == 'todos':
        livros = Livros.objects.all()  # Todos os livros
        # Requisição para buscar faixas populares de todos os gêneros
        DEEZER_POPULAR_TRACKS_URL = "https://api.deezer.com/chart/0/tracks"  # Pega as faixas populares de todos os gêneros
        response_faixas = requests.get(DEEZER_POPULAR_TRACKS_URL)
        if response_faixas.status_code == 200:
            try:
                faixas = response_faixas.json().get("data", [])
            except ValueError:
                faixas = []

        # Requisição para buscar artistas populares de todos os gêneros
        DEEZER_POPULAR_ARTISTS_URL = "https://api.deezer.com/chart/0/artists"  # Pega os artistas populares de todos os gêneros
        response_artistas = requests.get(DEEZER_POPULAR_ARTISTS_URL)
        if response_artistas.status_code == 200:
            try:
                artistas = response_artistas.json().get("data", [])
                # Organizando os artistas pela posição (position)
                artistas = sorted(artistas, key=lambda x: x.get('position', 0))  # Ordenando por position
            except ValueError:
                artistas = []

    else:
        genre_name = generos_dict.get(genre_id, "").lower()
        if genre_name:
            livros = Livros.objects.filter(genero__iexact=genre_name)

        # URL para faixas populares do gênero
        DEEZER_POPULAR_TRACKS_URL = f"https://api.deezer.com/chart/{genre_id}/tracks"

        # Requisição para buscar as faixas mais populares do gênero
        response_faixas = requests.get(DEEZER_POPULAR_TRACKS_URL)
        if response_faixas.status_code == 200:
            try:
                faixas = response_faixas.json().get("data", [])
            except ValueError:
                faixas = []

        # URL para artistas populares do gênero
        DEEZER_POPULAR_ARTISTS_URL = f"https://api.deezer.com/chart/{genre_id}/artists"

        # Realiza a requisição para a API Deezer para pegar os artistas mais populares
        response_artistas = requests.get(DEEZER_POPULAR_ARTISTS_URL)
        if response_artistas.status_code == 200:
            try:
                artistas = response_artistas.json().get("data", [])
                # Organizando os artistas pela posição (position)
                artistas = sorted(artistas, key=lambda x: x.get('position', 0))  # Ordenando por position
            except ValueError:
                artistas = []

    # Contexto atualizado
    context = {
        'generos': generos,  
        'faixas': faixas,  # Faixas populares do gênero selecionado ou de todos os gêneros
        'artistas': artistas,  # Artistas populares do gênero selecionado ou de todos os gêneros
        'livros': livros,  
        'livros_por_genero': livros_por_genero,  
        'genre_id': genre_id,  # Passa o ID do gênero para o template
    }

    return render(request, 'deezer_integration/genre_deezer.html', context)

