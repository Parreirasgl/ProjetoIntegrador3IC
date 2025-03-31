from datetime import date, datetime

from django import forms
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.models import Usuario

from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .models import Livros
from .serializers import LivroSerializer

from .forms import CadastroLivro, CategoriaLivro
from .models import Categoria, Emprestimos, Livros

import requests
from django.shortcuts import render

# Create your views here.

def home(request):
    usuario_id = request.session.get('usuario')

    if usuario_id:  
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            status_categoria = request.GET.get('cadastro_categoria')
            livros = Livros.objects.filter(usuario=usuario).order_by('obra')
            total_livros = livros.count()
            form = CadastroLivro()
            form.fields['usuario'].initial = usuario_id
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)
            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()
            livros_emprestar = Livros.objects.filter(usuario=usuario, emprestado=False)
            livros_emprestados = Livros.objects.filter(usuario=usuario, emprestado=True)

            # Recupera valores únicos para os campos de filtro
            obras = Livros.objects.filter(usuario=usuario).values_list('obra', flat=True).distinct()
            classificacoes = Livros.objects.filter(usuario=usuario).values_list('classificacao', flat=True).distinct()
            compositores = Livros.objects.filter(usuario=usuario).values_list('compositor', flat=True).distinct()
            arranjadores = Livros.objects.filter(usuario=usuario).values_list('arranjador', flat=True).distinct()

            # Aplica os filtros, se fornecidos na URL
            livros = Livros.objects.filter(usuario=usuario)

            # Aplica os filtros, se fornecidos na URL
            categoria_filtro = request.GET.get('categoria')
            obra_filtro = request.GET.get('obra')
            classificacao_filtro = request.GET.get('classificacao')
            compositor_filtro = request.GET.get('compositor')
            arranjador_filtro = request.GET.get('arranjador')

            if categoria_filtro:
                livros = livros.filter(categoria=categoria_filtro)
                # Se categoria foi filtrada, atualiza as obras disponíveis para essa categoria
                obras = livros.values_list('obra', flat=True).distinct()
                # Se obra não estiver na lista de obras disponíveis para a categoria, limpa o filtro de obra
                if obra_filtro and obra_filtro not in obras:
                    obra_filtro = None

            if obra_filtro:
                livros = livros.filter(obra=obra_filtro)

            if classificacao_filtro:
                livros = livros.filter(classificacao=classificacao_filtro)

            if compositor_filtro:
                livros = livros.filter(compositor=compositor_filtro)

            if arranjador_filtro:
                livros = livros.filter(arranjador=arranjador_filtro)



            return render(request, 'home.html', {
                'livros': livros,
                'usuario_logado': usuario_id,
                'form': form,
                'status_categoria': status_categoria,
                'form_categoria': form_categoria,
                'usuarios': usuarios,
                'livros_emprestar': livros_emprestar,
                'total_livro': total_livros,
                'livros_emprestados': livros_emprestados,
                'categorias': Categoria.objects.all(),
                'obras': obras,
                'classificacoes': classificacoes,
                'compositores': compositores,
                'arranjadores': arranjadores
            })
        except Usuario.DoesNotExist:
            # Usuário não encontrado, redireciona para a página de login
            return redirect('/auth/login/?status=2')
    else:
        # ID do usuário não está na sessão, redireciona para a página de login
        return redirect('/auth/login/?status=2')


def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id = id)
        if request.session.get('usuario') == livro.usuario.id:
            usuario = Usuario.objects.get(id = request.session['usuario'])
            categoria_livro = Categoria.objects.filter(usuario = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro = livro)
            form = CadastroLivro()
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
            
            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()

            livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)
            livros_emprestados = Livros.objects.filter(usuario = usuario).filter(emprestado = True)
            
            return render(request, 'ver_livro.html', {'livro': livro,
                                                      'categoria_livro': categoria_livro,
                                                      'emprestimos': emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form': form,
                                                      'id_livro': id,
                                                      'form_categoria': form_categoria,
                                                      'usuarios': usuarios,
                                                      'livros_emprestar': livros_emprestar,
                                                      'livros_emprestados': livros_emprestados})
        else:
            return HttpResponse('Esse livro não é seu')
    return redirect('/auth/login/?status=2')
    
def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('/livro/home')
        else:
            return HttpResponse('DADOS INVÁLIDOS')

def excluir_livro(request, id):
    livro = Livros.objects.get(id = id).delete()
    return redirect('/livro/home')

def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id = id_usuario)
        categoria = Categoria(nome = nome, descricao = descricao, usuario = user )
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse('Não foi desta vez.')

    
def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')
        #localizacao_retirada = request.POST.get('localizacao_retirada')
        
        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo = nome_emprestado_anonimo,
                                    livro_id = livro_emprestado)
        else:
            emprestimo = Emprestimos(nome_emprestado_id=nome_emprestado,
                                    livro_id = livro_emprestado)
        emprestimo.save()

        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()


        return redirect('/livro/home')

def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')
    livro_devolver = get_object_or_404(Livros, id=id)
    livro_devolver.emprestado = False
    livro_devolver.save()
    
    emprestimo_devolver = Emprestimos.objects.get(Q(livro = livro_devolver) & Q(data_devolucao = None) )
    emprestimo_devolver.data_devolucao = datetime.now()
    emprestimo_devolver.save()

    return redirect('/livro/home')

def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    compositor = request.POST.get('compositor')
    arranjador = request.POST.get('arranjador')
    obra = request.POST.get('obra')
    classificacao = request.POST.get('classificacao')
    conteudo = request.POST.get('conteudo')
    edicao = request.POST.get('edicao')
    localizacao = request.POST.get('localizacao')
    #exemplares_disponiveis = request.POST.get('exemplares_disponiveis')
    formato = request.POST.get('formato')
    observacao = request.POST.get('observacao')
    observacoes_gerais = request.POST.get('observacoes_gerais')

    categoria_id = request.POST.get('categoria_id')

    categoria = Categoria.objects.get(id = categoria_id)
    livro = Livros.objects.get(id = livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.compositor = compositor
        livro.arranjador = arranjador
        livro.obra = obra
        livro.classificacao = classificacao
        livro.conteudo = conteudo
        livro.edicao = edicao
        livro.localizacao = localizacao
        #livro.exemplares_disponiveis = exemplares_disponiveis
        livro.formato = formato
        livro.observacao = observacao
        livro.observacoes_gerais = observacoes_gerais

        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return redirect('/auth/sair')

def seus_emprestimos(request):
    usuario = Usuario.objects.get(id = request.session['usuario'])
    emprestimos = Emprestimos.objects.filter(nome_emprestado = usuario)
    


    return render(request, 'seus_emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                    'emprestimos': emprestimos})

def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')
    emprestimo = Emprestimos.objects.get(id = id_emprestimo)
    emprestimo.avaliacao = opcoes
    emprestimo.save()
    return redirect(f'/livro/ver_livro/{id_livro}')

class LivroList(APIView):
    def get(self, request):
        livros = Livros.objects.all()  # Obter todos os livros
        serializer = LivroSerializer(livros, many=True)  # Serializar os livros
        return Response(serializer.data, status=status.HTTP_200_OK)
    


#######################
# Função para buscar músicas populares de um gênero na Deezer
def search_deezer_genre(genre):
    url = f"https://api.deezer.com/genre/{genre}/artists"  # Exemplo de endpoint para artistas por gênero
    response = requests.get(url)
    data = response.json()
    
    artists = []
    for artist in data['data']:
        artists.append({
            'name': artist['name'],
            'id': artist['id'],
            'picture': artist['picture_medium'],  # Foto do artista
        })
    return artists

# View para exibir os artistas de um gênero
def genre_deezer(request, genre):
    artists = search_deezer_genre(genre)
    return render(request, 'deezer_integration/genre_deezer.html', {'artists': artists})