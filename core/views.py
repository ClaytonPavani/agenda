from django.shortcuts import render, redirect
from core.models import evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages

# Create your views here.

# def index(request):
#   return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou Senha inválido")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    Evento = evento.objects.filter(usuario=usuario)
    dados = {'Eventos': Evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def eventu(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['eventu'] = evento.objects.get(id=id_evento)
    return render(request, 'eventu.html', dados)

@login_required(login_url='/login/')
def submit_eventu(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        if id_evento:  # Verifica se é uma edição de evento existente
            eventu = evento.objects.get(id=id_evento)
            if eventu.usuario == usuario:  # Verifica se o usuário é o dono do evento
                eventu.titulo = titulo
                eventu.data_evento = data_evento
                eventu.descricao = descricao
                eventu.save()
        else:  # Caso contrário, cria um novo evento
            evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)

    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    eventu = evento.objects.get(id=id_evento)
    if usuario == eventu.usuario:
        eventu.delete()
    return redirect('/')

