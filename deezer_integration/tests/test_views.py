from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch, Mock

from deezer_integration.views import artistas_por_genero


class ArtistasPorGeneroViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('deezer_integration.views.requests.get')
    def test_view_get_todos_generos_sucesso(self, mock_get):
        # Simula a resposta da API de gêneros
        mock_get.return_value = Mock(status_code=200, json=lambda: {"data": [{"id": 1, "name": "Pop"}]})

        # Cria a requisição GET
        request = self.factory.get(reverse('artistas_por_genero'))
        response = artistas_por_genero(request)

        # Verifica se o status de resposta é 200 e se o conteúdo esperado está presente
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pop', response.content)


    @patch('deezer_integration.views.requests.get')
    # Simula escolha de gênero
    def test_view_post_genero_especifico(self, mock_get):
        # Mock da API de gêneros
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: {"data": [{"id": 1, "name": "Pop"}]}),  # gênero
            Mock(status_code=200, json=lambda: {"data": [{"title": "Música Pop 1"}]}),  # faixas
            Mock(status_code=200, json=lambda: {"data": [{"name": "Artista Pop", "position": 1}]})  # artistas
        ]

        request = self.factory.post(reverse('artistas_por_genero'), data={'genero': '1'})
        response = artistas_por_genero(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'M\xc3\xbasica Pop 1', response.content)  # Verifica se "Música Pop 1" está na resposta
        self.assertIn(b'Artista Pop', response.content)


    @patch('deezer_integration.views.requests.get')
    # testa o comportamento quando as APIs de faixas e artistas falham (ex: retornam 404)
    def test_faixas_populares_por_genero(self, mock_get):
        # Mock para gêneros
        mock_genero_response = Mock(status_code=200, json=lambda: {"data": [{"id": 152, "name": "Jazz"}]})
        # Mock para faixas populares do gênero
        mock_faixas_response = Mock(status_code=200, json=lambda: {"data": [{"title": "Take Five"}]})
        # Mock para artistas populares do gênero
        mock_artistas_response = Mock(status_code=200, json=lambda: {"data": [{"name": "Miles Davis", "position": 1}]})

        # Ordem esperada: gênero, faixas, artistas
        mock_get.side_effect = [mock_genero_response, mock_faixas_response, mock_artistas_response]

        # Simula requisição POST com genre_id = 152 (Jazz)
        request = self.factory.post(reverse('artistas_por_genero'), data={'genero': '152'})
        response = artistas_por_genero(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Take Five', response.content)
        self.assertIn(b'Miles Davis', response.content)

