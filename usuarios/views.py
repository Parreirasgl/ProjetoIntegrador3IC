import re
from hashlib import sha256

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Usuario

from django.shortcuts import render, redirect
from django.contrib import messages
from hashlib import sha256  # Assegure-se de importar sha256

def contato_view(request):
    return render(request, 'banda_sinfonica/contato.html')

def evento_view(request):
    return render(request, 'banda_sinfonica/eventos.html')

def galeria_view(request):
    return render(request, 'banda_sinfonica/galeria.html')

def login_view(request):
    return render(request, 'login.html')

def sobre_view(request):
    return render(request, 'banda_sinfonica/sobre.html')

def index_view(request):
    return render(request, 'banda_sinfonica/index.html')


def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None


def login(request):
    if request.session.get('usuario'):
        return redirect(f'/livro/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def cadastro(request):
    if request.session.get('usuario'):
        return redirect(f'/livro/home/')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')
    
    if not is_valid_email(email):
        return redirect('/auth/cadastro/?status=4')

    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome,
                          senha = senha,
                          email = email)
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')


def validar_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)

    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect(f'/livro/home/')

    # Resposta de fallback (geralmente não alcançada)
    return HttpResponse("Erro inesperado durante o login.")


def sair(request):
    request.session.flush()
    return redirect('/auth/login/')