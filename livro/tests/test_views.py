from django.test import TestCase
from livro.models import Usuario, Categoria  # Ajuste conforme necessário

class EmprestimosModelTest(TestCase):
    def setUp(self):
        # Criação de um usuário utilizando o modelo atual
        self.usuario = Usuario.objects.create(
            nome="testeuser",
            email="teste@teste.com",
            senha="teste123"  # Apenas uma string para a senha, sem necessidade de hashing
        )

    def test_categoria_criacao(self):
        # Teste de criação da categoria
        categoria = Categoria.objects.create(
            nome="Categoria Teste",
            descricao="Descrição Teste",
            usuario=self.usuario
        )

        self.assertIsNotNone(categoria.id)
        self.assertEqual(categoria.nome, "Categoria Teste")
        self.assertEqual(categoria.usuario, self.usuario)
