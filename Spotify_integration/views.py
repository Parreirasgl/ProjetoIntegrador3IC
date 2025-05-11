# spotify_integration/views.py
import requests
from django.shortcuts import render

SPOTIFY_TOKEN = "" 
SPOTIFY_POPULAR_TRACKS_URL = "https://api.spotify.com/v1/playlists/{}/tracks"

def obter_faixas_spotify(playlist_id):
    """Obtém as faixas populares de uma playlist no Spotify"""
    headers = {"Authorization": f"Bearer {SPOTIFY_TOKEN}"}
    url = SPOTIFY_POPULAR_TRACKS_URL.format(playlist_id)
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get("items", [])
            return [{
                "title": item["track"]["name"],
                "popularity": item["track"].get("popularity", 0)
            } for item in items]
    except Exception as e:
        print(f"Erro ao buscar faixas do Spotify: {e}")
    return []

def artistas_por_genero(request):
    """View para exibir faixas do Spotify e do Deezer"""
    faixas_spotify = []
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')  # Pegue o ID da playlist
        if playlist_id:
            faixas_spotify = obter_faixas_spotify(playlist_id)

    context = {
        'faixas_spotify': faixas_spotify,
    }
    return render(request, 'spotify_integration/genre_spotify.html', context)
