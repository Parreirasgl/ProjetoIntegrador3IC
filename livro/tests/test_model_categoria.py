from django.urls import reverse
from django.test import TestCase
from usuarios.models import Usuario
from ..models import Categoria

class CategoriaModelTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="testeuser",
            email="teste@teste.com",
            senha="teste123"  # senha em texto puro
        )
        # Configura o usuário na sessão para ser reutilizado nos testes
        session = self.client.session
        session['usuario'] = self.usuario.id
        session.save()


    def test_cadastrar_categoria_usuario_incorreto(self):
        response = self.client.post(reverse('cadastrar_categoria'), {
            'nome': 'Categoria Teste',
            'descricao': 'Descrição da categoria de teste',
            'usuario': '999',  # ID de usuário inválido
        })

        # Verifica se a resposta é 200 OK e se a categoria não foi criada
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Não foi desta vez.')  # Verifica a mensagem de erro
        self.assertFalse(Categoria.objects.filter(nome='Categoria Teste').exists())
        