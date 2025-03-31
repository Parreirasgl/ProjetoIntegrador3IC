from django.test import TestCase, Client
from django.urls import reverse
from livro.forms import CadastroLivro
from livro.models import Livros
from django.contrib.auth.models import User

class CadastrarLivroTest(TestCase):
    def setUp(self):
        # Cria um cliente de teste
        self.client = Client()

        # Cria um usuário para associar ao teste, caso necessário
        self.usuario = User.objects.create_user(username='teste_usuario', password='senha123')

        # URL para redirecionamento após o cadastro
        self.url = reverse('cadastrar_livro')

        # Dados válidos para o formulário de livro
        self.dados_validos = {
            'categoria': 'Categoria Exemplo',
            'compositor': 'Compositor Exemplo',
            'arranjador': 'Arranjador Exemplo',
            'obra': 'Sinfonia No.9',  # Alterei para verificar o campo 'obra'
            'classificacao': 'Classificação Exemplo',
            'conteudo': 'Conteúdo Exemplo',
            'edicao': '1ª',
            'observacao': 'Observação Exemplo',
            'data_cadastro': '2024-10-16',
            'emprestado': False,
            'localizacao': 'Localização Exemplo',
            'formato': 'Formato Exemplo',
            'usuario': self.usuario.id,
            'observacoes_gerais': 'Observações Gerais Exemplo',
        }

        # Dados inválidos para o formulário de livro (exemplo: obra vazia)
        self.dados_invalidos = {
            'categoria': 'Categoria Exemplo',
            'compositor': 'Compositor Exemplo',
            'arranjador': 'Arranjador Exemplo',
            'obra': '',  # 'obra' está vazio
            'classificacao': 'Classificação Exemplo',
            'conteudo': 'Conteúdo Exemplo',
            'edicao': '1ª',
            'observacao': 'Observação Exemplo',
            'data_cadastro': '2024-10-16',
            'emprestado': False,
            'localizacao': 'Localização Exemplo',
            'formato': 'Formato Exemplo',
            'usuario': self.usuario.id,
            'observacoes_gerais': 'Observações Gerais Exemplo',
        }

    def test_cadastrar_livro_dados_invalidos2(self):
        # Faz um POST com dados inválidos (exemplo: campo obrigatorio faltando)
        dados_invalidos = self.dados_validos.copy()
        dados_invalidos['compositor'] = ''  # Compositor está vazio, logo inválido

        response = self.client.post(self.url, dados_invalidos)

        # Verifica que não redirecionou e retornou um erro
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DADOS INVÁLIDOS')

        # Verifica que nenhum livro foi criado no banco de dados
        self.assertFalse(Livros.objects.filter(obra='Sinfonia No.9').exists())
