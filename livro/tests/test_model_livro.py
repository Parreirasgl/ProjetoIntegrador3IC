from django.test import TestCase
from usuarios.models import Usuario
from ..models import Categoria, Livros

class LivroModelTest(TestCase):
    
    def setUp(self):
        # Cria um usuário de teste
        self.usuario = Usuario.objects.create(
            nome="Usuario Teste",
            email="teste@email.com",
            senha="senha123"
        )
        
        # Cria uma categoria de teste
        self.categoria = Categoria.objects.create(
            nome="Ficção",
            descricao="Descrição de Ficção",
            usuario=self.usuario
        )
    
    def test_livro_criacao(self):
        """
        Testa se o livro é criado corretamente.
        """
        livro = Livros.objects.create(
            nome="Nome do Livro Teste",
            autor="Autor Teste",
            co_autor="Co-autor Teste",
            emprestado=False,
            categoria=self.categoria,
            usuario=self.usuario,
            localizacao="Estante A",
            exemplares_disponiveis="3",
            compositor="Compositor Teste",
            arranjador="Arranjador Teste",
            obra="Obra Teste",
            classificacao="Classificação Teste",
            conteudo="Conteúdo Teste",
            edicao="Edição Teste",
            observacao="Observação Teste",
            formato="Formato Teste"
        )
        
        # Verificações
        self.assertEqual(str(livro), livro.nome)
        self.assertEqual(livro.autor, "Autor Teste")
        self.assertFalse(livro.emprestado)
        self.assertEqual(livro.categoria, self.categoria)
        self.assertEqual(livro.usuario, self.usuario)
