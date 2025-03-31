from django.test import TestCase
from livro.forms import CadastroLivro
from datetime import date

class CadastroLivroFormTest(TestCase):
    
    def test_form_invalido_sem_nome(self):
        # Dados do formulário, sem o campo 'nome'
        form_data = {
            'categoria': 1,  # ID válido de uma categoria
            'compositor': 'Compositor Teste',
            'arranjador': 'Arranjador Teste',
            'obra': 'Obra Teste',
            'classificacao': 'Classificação Teste',
            'conteudo': 'Conteúdo Teste',
            'edicao': 'Edição Teste',
            'observacao': 'Observação Teste',
            'data_cadastro': date.today(),
            'emprestado': False,
            'localizacao': 'Localização Teste',
            'formato': 'Formato Teste',
            'usuario': 1,  # ID válido de um usuário
            'observacoes_gerais': 'Observações gerais Teste'
        }
        form = CadastroLivro(data=form_data)
        
        # Verifique se o formulário é inválido sem o campo 'nome'
        self.assertFalse(form.is_valid())
