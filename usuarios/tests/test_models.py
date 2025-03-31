# Testes de model
from django.core.exceptions import ValidationError
from django.test import TestCase
from usuarios.models import Usuario  # Importa o modelo correto
from ..models import Usuario
from ..admin import UsuarioAdmin

class UsuarioModelTest(TestCase):

    def test_criacao_de_usuario_simples(self):
        """Testa a criação simples de um usuário."""
        usuario = Usuario.objects.create(
            nome='Teste Simples',
            email='teste.simples@email.com',
            senha='senha123',
            ativo=True
        )
        
        # Verifica se o usuário foi criado e se os atributos estão corretos
        self.assertIsInstance(usuario, Usuario)
        self.assertEqual(usuario.nome, 'Teste Simples')
        self.assertEqual(usuario.email, 'teste.simples@email.com')
        self.assertTrue(usuario.ativo)

    def test_email_unico(self):
        """Testa se o email do usuário é único."""
        Usuario.objects.create(nome='Usuario Existente', email='teste@exemplo.com', senha='senha123', ativo=True)
        usuario2 = Usuario(nome='Outro Usuario', email='teste@exemplo.com', senha='senha123', ativo=True)  # Cria outro usuário com o mesmo email

        with self.assertRaises(ValidationError):
            usuario2.full_clean()  # Verifica se o método full_clean levanta o ValidationError

    def test_nome_vazio(self):
        """Testa a validação para nome vazio."""
        usuario = Usuario(nome='', email='test@email.com', senha='senha123', ativo=True)
        with self.assertRaises(ValidationError):
            usuario.full_clean()

    def test_senha_vazia(self):
        """Testa a validação para senha vazia."""
        usuario = Usuario(nome='Usuario', email='test@email.com', senha='', ativo=True)
        with self.assertRaises(ValidationError):
            usuario.full_clean()

    def test_email_invalido(self):
        """Testa a validação para email inválido."""
        usuario = Usuario(nome='Usuario', email='invalid-email', senha='senha123', ativo=True)
        with self.assertRaises(ValidationError):
            usuario.full_clean()

    def test_str_method(self):
        """Testa o método __str__ do usuário."""
        usuario = Usuario.objects.create(nome='Teste Simples', email='teste.simples@email.com', senha='senha123', ativo=True)
        self.assertEqual(str(usuario), 'Teste Simples')

    def test_atualizacao_usuario(self):
        """Testa a atualização de um usuário existente."""
        usuario = Usuario.objects.create(nome='Usuario Original', email='original@email.com', senha='senha123', ativo=True)
        usuario.nome = 'Usuario Atualizado'
        usuario.save()
        self.assertEqual(usuario.nome, 'Usuario Atualizado')

    def test_deletar_usuario(self):
        """Testa a exclusão de um usuário."""
        usuario = Usuario.objects.create(nome='Usuario Para Deletar', email='delete@email.com', senha='senha123', ativo=True)
        usuario.delete()
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(email='delete@email.com')

    def test_usuario_ativo(self):
        """Testa se o usuário está ativo."""
        usuario = Usuario.objects.create(nome='Usuario Ativo', email='ativo@email.com', senha='senha123', ativo=True)
        self.assertTrue(usuario.ativo)

    def test_usuario_inativo(self):
        """Testa se o usuário está inativo."""
        usuario = Usuario.objects.create(nome='Usuario Inativo', email='inativo@email.com', senha='senha123', ativo=False)
        self.assertFalse(usuario.ativo)
