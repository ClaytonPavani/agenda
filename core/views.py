from django.shortcuts import render
from core.models import evento

# Create your views here.

# def index(request):
#   return redirect('/agenda/')
def lista_eventos(request):
    usuario = request.user
    Evento = evento.objects.all()
    dados = {'Eventos': Evento}
    return render(request, 'agenda.html', dados)