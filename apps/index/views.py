from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index/index.html')

def login_view(request):
    return render(request, "login/login.html")

def cadastro_cooperativa(request):
    return render(request, "cadastro_cooperativa/cadastro_cooperativa.html")

def cadastro_gestor(request):
    return render(request, "cadastro_gestor/cadastro_gestor.html")