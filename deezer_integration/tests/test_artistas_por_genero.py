from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock

class ArtistasPorGeneroViewIntegrationTest(TestCase):
    @patch('deezer_integration.views.requests.get')
    def test_artistas_por_genero_view_integration(self, mock_get):
        # Simula a resposta da API do Deezer
        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "data": [
                {"id": 1, "name": "Artist 1", "position": 1},
                {"id": 2, "name": "Artist 2", "position": 2}
            ]
        })

        # Faz a requisição para a view (essa é a integração com a API externa)
        client = Client()
        response = client.get(reverse('artistas_por_genero'))  # Substitua pelo nome correto da URL

        # Verifica se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se o conteúdo retornado pela view contém dados da resposta da API
        self.assertIn(b'Artist 1', response.content)
        self.assertIn(b'Artist 2', response.content)

    @patch('deezer_integration.views.requests.get')
    def test_artistas_por_genero_view_com_erro_api(self, mock_get):
        mock_get.return_value = Mock(status_code=500)

        client = Client()
        response = client.get(reverse('artistas_por_genero'))

        self.assertEqual(response.status_code, 200)
        
        # Verifica se o template padrão ainda está sendo exibido
        self.assertIn(b'Escolha o g\xc3\xaanero:', response.content)

