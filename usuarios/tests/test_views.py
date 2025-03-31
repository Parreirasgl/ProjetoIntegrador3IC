from django.shortcuts import redirect, render
from django.test import TestCase, Client
from django.urls import reverse
from hashlib import sha256

from requests import patch
from usuarios.models import Usuario
from livro.models import Livros, Categoria  # Ajuste na importação
import re


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()


        # Criação do usuário com senha criptografada conforme esperado pela view
        self.usuario = Usuario.objects.create(
            nome='Test User',
            email='test@example.com',
            senha=sha256('12345'.encode()).hexdigest(),  # senha criptografada
            ativo=True
        )

        # # Simulando login do usuário com a senha criptografada
        # session = self.client.session
        # session['usuario'] = self.usuario.id
        # session.save()

        # Criar outras instâncias de teste
        self.categoria = Categoria.objects.create(nome='Test Categoria', usuario=self.usuario)
        self.livro = Livros.objects.create(
            nome='O Grande Gatsby',
            autor='F. Scott Fitzgerald',
            categoria=self.categoria,
            usuario=self.usuario,
            localizacao='Estante A',
            exemplares_disponiveis='5'
        )

    def test_valida_cadastro_email_invalido(self):
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Novo Usuario',
            'email': 'emailinvalido',
            'senha': 'senha1234'
        })
        self.assertEqual(response.status_code, 302)

    def test_valida_cadastro_email_ja_existente(self):
        """Testa se um email já existente no banco de dados é rejeitado."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Novo Usuario',
            'email': 'test@example.com',  # Email já criado no setUp
            'senha': 'senha1234'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se o código de status é 302
        self.assertEqual(response['Location'], '/auth/cadastro/?status=3')  # Verifica se o redirecionamento foi para a URL correta

    def test_valida_cadastro_senha_curta(self):
        """Testa se uma senha com menos de 8 caracteres é rejeitada."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Usuario',
            'email': 'test@example.com',
            'senha': '123'  # Senha muito curta
        })
        self.assertEqual(response.status_code, 302)  # Verifica se o redirecionamento ocorreu (302)
        self.assertEqual(response['Location'], '/auth/cadastro/?status=2')  # Verifica a URL de redirecionamento

    def test_valida_cadastro_nome_ou_email_vazio(self):
        """Testa se campos nome ou email vazios são rejeitados."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': '',  # Nome vazio
            'email': 'test@example.com',
            'senha': 'senha1234'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se o redirecionamento ocorreu (302)
        self.assertEqual(response['Location'], '/auth/cadastro/?status=1')  # Verifica a URL de redirecionamento

    def test_sair(self):
        # Chamar a view de logout
        response = self.client.get(reverse('sair'))

        # Verifique se a sessão foi limpa
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/')
        # Verifique se a sessão foi realmente limpa
        self.assertFalse('_auth_user_id' in self.client.session)

    #Cadastro
    def test_cadastro_usuario_logado(self):
        # Simulando um usuário logado na sessão
        session = self.client.session
        session['usuario'] = 1  # Id de um usuário fictício
        session.save()

        # Faz a requisição para a view de cadastro
        response = self.client.get(reverse('cadastro'))

        # Verifica se o usuário foi redirecionado para a página /livro/home/
        self.assertRedirects(response, '/livro/home/')

    def test_cadastro_usuario_deslogado(self):
        # Simulando um usuário deslogado (sem sessão)
        session = self.client.session
        session.pop('usuario', None)  # Remover qualquer dado de sessão do usuário
        session.save()

        # Faz a requisição para a view de cadastro
        response = self.client.get(reverse('cadastro'))

        # Verifica se a página de cadastro foi carregada corretamente
        self.assertEqual(response.status_code, 200)

        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_cadastro_com_status(self):
        # Simulando um usuário deslogado (sem sessão)
        session = self.client.session
        session.pop('usuario', None)  # Remove a sessão de usuário se houver
        session.save()

        # Faz a requisição para a view de cadastro com um status na URL
        response = self.client.get(reverse('cadastro') + '?status=1')

        # Verifica se a página de cadastro foi carregada corretamente
        self.assertEqual(response.status_code, 200)

        # Verifica se o status foi passado corretamente para o template
        self.assertIn('status', response.context)
        self.assertEqual(response.context['status'], '1')

        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'cadastro.html')

        # Verifica se a página de cadastro foi carregada corretamente
        self.assertEqual(response.status_code, 200)

        # Verifica se o status foi passado corretamente para o template
        self.assertIn('status', response.context)
        self.assertEqual(response.context['status'], '1')

        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'cadastro.html')

        # Verifica as views do frontend
    def test_contato_view(self):
        response = self.client.get(reverse('contato'))  # Nome da URL que mapeia para contato_view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banda_sinfonica/contato.html')

    def test_evento_view(self):
        response = self.client.get(reverse('evento'))  # Nome da URL que mapeia para evento_view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banda_sinfonica/eventos.html')

    def test_galeria_view(self):
        response = self.client.get(reverse('galeria'))  # Nome da URL que mapeia para galeria_view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banda_sinfonica/galeria.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))  # Nome da URL que mapeia para login_view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_sobre_view(self):
        response = self.client.get(reverse('sobre'))  # Nome da URL que mapeia para sobre_view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banda_sinfonica/sobre.html')

    def test_index_view(self):
        response = self.client.get(reverse('index'))  # Nome da URL que mapeia para index_view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'banda_sinfonica/index.html')
    
    def test_login_render_login_template_for_unauthenticated_user(self):
        response = self.client.get(reverse('login'))  # Acesse a URL de login

        # Verifique se o template correto foi usado
        self.assertTemplateUsed(response, 'login.html')  # Certifique-se de que você está verificando o template correto

        # Verifique se 'status' está como None
        self.assertIsNone(response.context.get('status'))  # Use .get() para evitar KeyError

    def test_valida_cadastro_usuario_valido(self):
        """Testa se um usuário é cadastrado corretamente."""
        # Dados válidos para cadastro
        dados = {
            'nome': 'Novo Usuario',
            'email': 'usuario@exemplo.com',
            'senha': 'senha1234'
        }
        
        # Chama a view de validação de cadastro
        response = self.client.post(reverse('valida_cadastro'), dados)

        # Verifica se o redirecionamento foi para o status 0 (cadastrado com sucesso)
        self.assertRedirects(response, '/auth/cadastro/?status=0')

        # Verifica se o usuário foi criado no banco de dados
        usuario = Usuario.objects.get(email='usuario@exemplo.com')
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nome, 'Novo Usuario')
        # Você pode também verificar se a senha foi corretamente armazenada (embora criptografada)
        self.assertEqual(usuario.senha, sha256('senha1234'.encode()).hexdigest())
