from django.test import TestCase
from django.urls import reverse
from usuarios.models import Usuario  # Supondo que sua model de usuário se chama 'Usuario'
from hashlib import sha256

class ValidarLoginTest(TestCase):
    
    def setUp(self):
        # Criando um usuário de teste
        senha = sha256('senha123'.encode()).hexdigest()  # Senha criptografada
        self.usuario = Usuario.objects.create(email='teste@email.com', senha=senha)
        self.url_login = reverse('validar_login')  # Ajuste o nome da URL se necessário

    def test_validar_login_com_sucesso(self):
        # Dados corretos para login
        dados = {
            'email': 'teste@email.com',
            'senha': 'senha123',  # Senha em texto simples (vai ser criptografada na view)
        }

        # Fazer requisição POST com os dados corretos
        response = self.client.post(self.url_login, dados)

        # Verificar redirecionamento para a home do livro após login com sucesso
        self.assertRedirects(response, '/livro/home/')

        # Verificar se o usuário foi salvo na sessão
        self.assertEqual(self.client.session['usuario'], self.usuario.id)

    def test_validar_login_falha(self):
        # Dados incorretos para login
        dados = {
            'email': 'teste@email.com',
            'senha': 'senha_errada',
        }

        # Fazer requisição POST com dados incorretos
        response = self.client.post(self.url_login, dados)

        # Verificar redirecionamento para a página de login com status=1 (falha)
        self.assertRedirects(response, '/auth/login/?status=1')

        # Verificar se o usuário NÃO foi salvo na sessão
        self.assertNotIn('usuario', self.client.session)

    def test_validar_login_usuario_inexistente(self):
        # Tentando fazer login com um email que não existe
        dados = {
            'email': 'nao_existe@email.com',
            'senha': 'senha123',
        }

        # Fazer requisição POST com dados inexistentes
        response = self.client.post(self.url_login, dados)

        # Verificar redirecionamento para a página de login com status=1 (falha)
        self.assertRedirects(response, '/auth/login/?status=1')

        # Verificar se o usuário NÃO foi salvo na sessão
        self.assertNotIn('usuario', self.client.session)

