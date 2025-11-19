from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.db import connection
from .models import Gestor, Cooperativa, OperadorArmazem

# Create your views here.
def index(request):
    return render(request, 'index/index.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password") or ""

        usuario_encontrado = None
        tipo_usuario = None

        if username:
            gestor = None

            
            try:
                gestor = Gestor.objects.get(usuario=username)
            except Gestor.DoesNotExist:
                try:
                    gestor = Gestor.objects.get(email=username)
                except Gestor.DoesNotExist:
                    gestor = None

            if gestor and check_password(password, gestor.senha_hash):
                usuario_encontrado = gestor
                tipo_usuario = "gestor"

        
        if usuario_encontrado is None and username:
            coop = None
            try:
                coop = Cooperativa.objects.get(usuario=username)
            except Cooperativa.DoesNotExist:
                try:
                    coop = Cooperativa.objects.get(cnpj=username)
                except Cooperativa.DoesNotExist:
                    coop = None

            if coop and check_password(password, coop.senha_hash):
                usuario_encontrado = coop
                tipo_usuario = "cooperativa"


        if usuario_encontrado is None and username:
            op = None
            try:
                op = OperadorArmazem.objects.get(usuario=username)
            except OperadorArmazem.DoesNotExist:
                op = None

            if op and check_password(password, op.senha_hash):
                usuario_encontrado = op
                tipo_usuario = "operador"


        if usuario_encontrado is not None:
            request.session["user_tipo"] = tipo_usuario
            request.session["user_id"] = usuario_encontrado.pk

            messages.success(
                request,
                f"Login realizado com sucesso como {tipo_usuario.title()}!"
            )

            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha incorretos.")


    return render(request, "login/login.html")

def cadastro_cooperativa(request):
    if request.method == "POST":
        usuario       = request.POST.get("usuario", "").strip()
        nome_fantasia = request.POST.get("nome_fantasia", "").strip()
        cnpj          = request.POST.get("cnpj", "").strip()
        email         = request.POST.get("email", "").strip()
        telefone      = request.POST.get("telefone", "").strip()
        usuario       = request.POST.get("usuario", "").strip()
        endereco      = request.POST.get("endereco", "").strip()  # rua
        numero        = request.POST.get("numero", "").strip()
        bairro        = request.POST.get("bairro", "").strip()
        cidade        = request.POST.get("cidade", "").strip()
        cep           = request.POST.get("cep", "").strip()

        senha         = request.POST.get("senha")
        confirmar     = request.POST.get("confirmar_senha")

        erros = []
        if len(cnpj) > 18:
            erros.append("CNPJ muito longo. Verifique o formato.")
        # obrigatórios
        if not all([usuario, nome_fantasia, cnpj, email, endereco,
                    numero, bairro, cidade, cep, senha, confirmar]):
            erros.append("Preencha todos os campos obrigatórios.")

        if senha != confirmar:
            erros.append("As senhas não conferem.")

        if Cooperativa.objects.filter(cnpj=cnpj).exists():
            erros.append("Já existe uma cooperativa registrada com esse CNPJ.")

        if Cooperativa.objects.filter(emailinstitucional=email).exists():
            erros.append("Já existe uma cooperativa registrada com esse e-mail.")

        if Cooperativa.objects.filter(usuario=usuario).exists():
            erros.append("Já existe uma cooperativa registrada com esse usuário.")

        if erros:
            for e in erros:
                messages.error(request, e)
            return render(request, "cadastro_cooperativa/cadastro_cooperativa.html")

        # gera hash da senha
        senha_hash = make_password(senha)

        # por enquanto usamos o nome fantasia também como nomeResponsavel
        nome_responsavel = usuario
        cpf_responsavel = None   # campo é NULL na tabela

        # UF e complemento: como não estão no form, uso valores fixos/vasios por enquanto
        uf = "PE"      # você pode trocar depois ou adicionar campo UF no formulário
        comp = ""      # complemento opcional

        # chama a procedure
        with connection.cursor() as cursor:
            cursor.callproc(
                "cadCooperativa_tel_endereco",
                [
                    cnpj,
                    nome_fantasia,
                    nome_responsavel,
                    cpf_responsavel,
                    email,
                    senha_hash,
                    usuario,
                    telefone,
                    uf,
                    cidade,
                    bairro,
                    endereco,
                    int(numero) if numero.isdigit() else 0,
                    comp,
                    cep,
                ]
            )

        messages.success(request, "Cooperativa cadastrada com sucesso! Agora você já pode fazer login.")
        return redirect("login_view")

    # GET
    return render(request, "cadastro_cooperativa/cadastro_cooperativa.html")

def cadastro_gestor(request):
    if request.method == "POST":
        nome = request.POST.get("nome_completo","").strip()
        usuario = request.POST.get("usuario", "").strip()
        cpf = request.POST.get("cpf", "").strip()
        email = request.POST.get("email", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        senha = request.POST.get("senha")
        confirmar = request.POST.get("confirmar_senha")

        erros = []

        if not nome or not cpf or not email or not senha or not confirmar or not usuario:
            erros.append("Preencha todos os campos obrigatórios.")
        
        if senha != confirmar:
            erros.append("As senhas não conferem.")
        
        if Gestor.objects.filter(cpf=cpf).exists():
            erros.append("Já existe um gestor registrado com esse CPF.")

        if Gestor.objects.filter(email=email).exists():
            erros.append("Já existe um gestor registrado com esse e-mail.")
        
        if erros:
            for e in erros:
                messages.error(request, e)
            return render(request, "cadastro_gestor/cadastro_gestor.html")
        
        senha_hash = make_password(senha)

        with connection.cursor() as cursor:
            cursor.callproc(
                "cadGestor_telefone",
                [cpf, nome, email, senha_hash, usuario, telefone]
            )
        messages.success(request, "Cadastro realizado com sucesso! Agora você já pode fazer login.")

        return redirect("login_view")
    return render(request, "cadastro_gestor/cadastro_gestor.html")

def gestao_cooperativa(request):
    return render(request, "GestaoCooperativa/GestaoCooperativa.html")


def home(request):
    return render(request, "Home/Home.html")
