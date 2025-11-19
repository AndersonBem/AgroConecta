from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.db import connection
from .models import (Gestor, Cooperativa, OperadorArmazem, Telefone, TipoSemente,
                     Solicitacao)
from django.db.models import Count

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

   # GET → só abrir o formulário em modo criação
    context = {
        "modo": "criar",
        "coop": None,
        "telefone": "",
    }
    return render(request, "cadastro_cooperativa/cadastro_cooperativa.html", context)

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

def gestao_cooperativas(request):
    # Conta quantas solicitações cada cooperativa tem
    cooperativas = (
        Cooperativa.objects
        .annotate(total_solicitacoes=Count('solicitacao'))  # nome da relação reversa
        .order_by('razaosocial')
    )

    context = {
        "cooperativas": cooperativas,
        
    }
    return render(request, "GestaoCooperativa/GestaoCooperativa.html", context)

def editar_cooperativa(request, cnpj):
    # busca cooperativa ou 404
    coop = get_object_or_404(Cooperativa, pk=cnpj)

    # telefone principal (pega o primeiro cadastrado)
    telefone_atual = (
        Telefone.objects
        .filter(cooperativa_cnpj=coop)
        .values_list("numero", flat=True)
        .first()
    )

    if request.method == "POST":
        # ---------- 1. Coleta dados do formulário ----------
        usuario       = request.POST.get("usuario", "").strip()
        nome_fantasia = request.POST.get("nome_fantasia", "").strip()
        # cnpj_form   = request.POST.get("cnpj", "").strip()  # não vamos permitir mudar o CNPJ
        email         = request.POST.get("email", "").strip()
        telefone      = request.POST.get("telefone", "").strip()
        endereco      = request.POST.get("endereco", "").strip()  # rua
        numero        = request.POST.get("numero", "").strip()
        bairro        = request.POST.get("bairro", "").strip()
        cidade        = request.POST.get("cidade", "").strip()
        cep           = request.POST.get("cep", "").strip()

        senha         = request.POST.get("senha") or ""
        confirmar     = request.POST.get("confirmar_senha") or ""

        erros = []

        # ---------- 2. Validações básicas ----------
        if not all([usuario, nome_fantasia, email, endereco,
                    numero, bairro, cidade, cep]):
            erros.append("Preencha todos os campos obrigatórios (exceto senha).")

        # senha opcional: se preencher, tem que conferir
        if senha or confirmar:
            if senha != confirmar:
                erros.append("As senhas não conferem.")
        # se não preencher, mantemos a senha atual

        # CNPJ: não permitimos alterar (melhor deixar read-only no template)
        # if cnpj_form != coop.cnpj:
        #     erros.append("O CNPJ não pode ser alterado.")

        # email duplicado (exceto a própria cooperativa)
        if (
            Cooperativa.objects
            .filter(emailinstitucional=email)
            .exclude(pk=coop.pk)
            .exists()
        ):
            erros.append("Já existe outra cooperativa registrada com esse e-mail.")

        # usuario duplicado (exceto a própria cooperativa)
        if (
            Cooperativa.objects
            .filter(usuario=usuario)
            .exclude(pk=coop.pk)
            .exists()
        ):
            erros.append("Já existe outra cooperativa registrada com esse usuário.")

        # número do endereço
        if not numero.isdigit():
            erros.append("O número do endereço deve conter apenas dígitos.")

        # se houver erros, mostra e volta pro template com dados atuais
        if erros:
            for e in erros:
                messages.error(request, e)

            context = {
                "modo": "editar",
                "coop": coop,
                "telefone": telefone,
            }
            return render(request, "cadastro_cooperativa/cadastro_cooperativa.html", context)

        # ---------- 3. Definição da senha_hash ----------
        if senha:
            # usuário digitou nova senha -> gera novo hash
            senha_hash = make_password(senha)
        else:
            # mantém a senha atual
            senha_hash = coop.senha_hash

        # ---------- 4. Campos que não vêm do formulário ----------
        # por enquanto vamos manter o nomeResponsavel e cpfResponsavel atuais
        nome_responsavel = coop.nomeresponsavel
        cpf_responsavel  = coop.cpfresponsavel

        # UF e complemento (por enquanto fixos / vazios)
        uf   = "PE"
        comp = ""

        # ---------- 5. Chama a procedure de UPDATE ----------
        with connection.cursor() as cursor:
            cursor.callproc(
                "updCooperativa_tel_endereco",
                [
                    coop.cnpj,                # p_cnpj - não alteramos
                    nome_fantasia,           # p_razaoSocial
                    nome_responsavel,        # p_nomeResponsavel
                    cpf_responsavel,         # p_cpfResponsavel
                    email,                   # p_emailInst
                    senha_hash,              # p_senha_hash
                    usuario,                 # p_usuario
                    telefone,                # p_telefone

                    uf,                      # p_uf
                    cidade,                  # p_cidade
                    bairro,                  # p_bairro
                    endereco,                # p_rua
                    int(numero),             # p_numero
                    comp,                    # p_comp
                    cep,                     # p_cep
                ]
            )

        messages.success(request, "Cooperativa atualizada com sucesso!")
        return redirect("gestao_cooperativa")

    # ---------- GET: só exibe o formulário preenchido ----------
    context = {
        "modo": "editar",
        "coop": coop,
        "telefone": telefone_atual or "",
    }
    return render(request, "cadastro_cooperativa/cadastro_cooperativa.html", context)

def ver_cooperativa(request, cnpj):
    """
    Mostra os detalhes de uma cooperativa específica:
    dados básicos, endereço, telefones e solicitações.
    """

    # Cooperativa + endereço (FK Endereco)
    cooperativa = get_object_or_404(
        Cooperativa.objects.select_related("endereco_idendereco"),
        cnpj=cnpj
    )

    # Telefones ligados à cooperativa
    telefones = Telefone.objects.filter(cooperativa_cnpj=cooperativa)

    # Solicitações da cooperativa (pode limitar pra não vir milhões)
    solicitacoes_qs = (
        Solicitacao.objects
        .filter(cooperativa_cnpj=cooperativa)
        .select_related("safra_idsafra", "status_idstatus")  # ajuste nomes se forem diferentes
        .order_by("-idsolicitacao")                          # ou "-idSolicitacao", depende do model
    )

    total_solicitacoes = solicitacoes_qs.count()
    solicitacoes = solicitacoes_qs[:10]  # por exemplo: mostra só as 10 mais recentes

    context = {
        "coop": cooperativa,
        "telefones": telefones,
        "solicitacoes": solicitacoes,
        "total_solicitacoes": total_solicitacoes,
    }

    return render(request, "VerCooperativa/VerCooperativa.html", context)

def gestao_sementes(request):
    # Conta quantas solicitações cada cooperativa tem
    sementes = TipoSemente.objects.all
    

    context = {"sementes": sementes}
    return render(request, "GestaoSementes/GestaoSementes.html", context)

def cadastrar_semente(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        erros = []

        if not nome:
            erros.append("O nome da semente é obrigatório.")

        if TipoSemente.objects.filter(nome=nome).exists():
            erros.append("Já existe uma semente cadastrada com esse nome.")

        if erros:
            for e in erros:
                messages.error(request, e)
            return render(request, "semente/cadastrar_semente.html")

        TipoSemente.objects.create(
            nome=nome,
            descricao=descricao if descricao else None
        )

        messages.success(request, "Semente cadastrada com sucesso!")
        return redirect("gestao_sementes")

    return render(request, "cadastro_semente/cadastro_semente.html")

def editar_semente(request, id):
    # Busca a semente pelo ID ou retorna 404
    semente = get_object_or_404(TipoSemente, idtiposemente=id)

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        erros = []

        # Nome obrigatório
        if not nome:
            erros.append("O nome da semente é obrigatório.")

        # Verifica duplicidade (exceto ela mesma)
        if TipoSemente.objects.filter(nome=nome).exclude(idtiposemente=id).exists():
            erros.append("Já existe uma semente cadastrada com esse nome.")

        if erros:
            for e in erros:
                messages.error(request, e)
            return render(request, "semente/editar_semente.html", {"semente": semente})

        # Atualiza
        semente.nome = nome
        semente.descricao = descricao if descricao else None
        semente.save()

        messages.success(request, "Semente atualizada com sucesso!")

        return redirect("gestao_sementes")  # ajuste conforme sua lista

    return render(request, "semente/editar_semente.html", {"semente": semente})

def detalhes_semente(request, id):
    # busca a semente pelo ID (idtiposemente é a PK)
    semente = get_object_or_404(TipoSemente, idtiposemente=id)

    contexto = {
        "semente": semente,
    }
    return render(request, "semente/detalhes_semente.html", contexto)

def home(request):
    return render(request, "Home/Home.html")

def gestao_sementes(request):
    return render(request, "GestaoSementes/GestaoSementes.html")