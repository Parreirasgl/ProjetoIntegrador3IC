from datetime import date

from django import forms
from django.db import models
from django.db.models import fields

from usuarios.models import Usuario

from .models import Categoria, Emprestimos, Livros


class CadastroLivro(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ['categoria','compositor', 'arranjador', 'obra', 'classificacao', 'conteudo', 'edicao', 'edicao', 'observacao', 'data_cadastro', 'emprestado', 'localizacao', 'categoria', 'formato', 'usuario', 'observacoes_gerais', 'genero']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()

class CategoriaLivro(forms.Form):
    nome = forms.CharField(max_length=30)
    descricao = forms.CharField(max_length=60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget = forms.Textarea()

class EventoForm(forms.Form):
    summary = forms.CharField(max_length=255)
    location = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    start_datetime = forms.DateTimeField()
    end_datetime = forms.DateTimeField()
    attendees_emails = forms.CharField(help_text="Separe os e-mails com vírgulas")