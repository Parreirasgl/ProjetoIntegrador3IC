# tests.py

from django.test import SimpleTestCase
from datetime import datetime, timedelta
from ..templatetags.filtros import mostra_duracao  # type: ignore # Altere 'seu_modulo' para o nome do seu módulo de template

class MostraDuracaoTest(SimpleTestCase):
    def test_mostra_duracao_dias(self):
        # Testa a diferença de dias
        data1 = datetime(2024, 11, 10)  # Data futura
        data2 = datetime(2024, 11, 5)   # Data passada
        resultado = mostra_duracao(data1, data2)
        self.assertEqual(resultado, "5 Dias.")  # Verifica se a saída está correta

    def test_mostra_duracao_um_dia(self):
        # Testa a diferença de 1 dia
        data1 = datetime(2024, 11, 10)
        data2 = datetime(2024, 11, 9)
        resultado = mostra_duracao(data1, data2)
        self.assertEqual(resultado, "1 Dia.")  # Verifica se a saída está correta para 1 dia

    def test_mostra_duracao_data_nao_devolvida(self):
        # Testa o caso em que as datas não são válidas
        resultado = mostra_duracao(None, None)  # Passando None
        self.assertEqual(resultado, "Ainda não foi devolvido.")  # Verifica se a saída está correta

    def test_mostra_duracao_dados_invalidos(self):
        # Testa o caso em que os valores não são datetimes
        resultado = mostra_duracao("texto", "texto")
        self.assertEqual(resultado, "Ainda não foi devolvido.")  # Verifica se a saída está correta

    def test_mostra_duracao_dias_negativos(self):
        # Testa a diferença de dias negativos
        data1 = datetime(2024, 11, 5)
        data2 = datetime(2024, 11, 10)
        resultado = mostra_duracao(data2, data1)
        self.assertEqual(resultado, "5 Dias.")  # A diferença em dias ainda deve ser 5
