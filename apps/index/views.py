from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.db import connection
from .models import (Gestor, Cooperativa, OperadorArmazem, Telefone, TipoSemente,
                     Solicitacao,Armazem, Lote, Endereco)
from django.db.models import Count, Sum

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

def detalhe_cooperativa(request, cnpj):

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

    return render(request, "verCooperativa/verCooperativa.html", context)

def gestao_sementes(request):

    sementes = TipoSemente.objects.all()

    sementes_info = []

    for seed in sementes:
        # Lotes dessa semente
        lotes = Lote.objects.filter(tiposemente_idtiposemente=seed.idtiposemente)

        # Soma total em Kg
        total_kg = lotes.aggregate(total=Sum("peso"))["total"] or 0

        # Armazéns que possuem essa semente
        armazens = Armazem.objects.filter(
            idarmazem__in=lotes.values("armazem_idarmazem")
        ).values_list("nome", flat=True).distinct()

        # Status
        status = "Em estoque" if lotes.exists() else "Em falta"

        sementes_info.append({
            "obj": seed,
            "total_kg": total_kg,
            "armazens": list(armazens),
            "status": status,
        })

    return render(request, "GestaoSementes/GestaoSementes.html", {
        "sementes": sementes_info
    })

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
            return render(request, "GestaoSementes/cadastrar_semente.html")

        TipoSemente.objects.create(
            nome=nome,
            descricao=descricao if descricao else None
        )

        messages.success(request, "Semente cadastrada com sucesso!")
        return redirect("gestao_sementes")

    return render(request, "GestaoSementes/cadastrar_semente.html")

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
            return render(request, "GestaoSementes/editar_semente.html", {"semente": semente})

        # Atualiza
        semente.nome = nome
        semente.descricao = descricao if descricao else None
        semente.save()

        messages.success(request, "Semente atualizada com sucesso!")

        return redirect("gestao_sementes")  # ajuste conforme sua lista

    return render(request, "GestaoSementes/editar_semente.html", {"semente": semente})

def detalhes_semente(request, id):
    # busca a semente pelo ID (idtiposemente é a PK)
    semente = get_object_or_404(TipoSemente, idtiposemente=id)

    # lotes dessa semente
    lotes = Lote.objects.filter(tiposemente_idtiposemente=semente.idtiposemente)

    # armazéns que possuem essa semente
    armazens = Armazem.objects.filter(
        idarmazem__in=lotes.values("armazem_idarmazem")
    ).values_list("nome", flat=True).distinct()

    contexto = {
        "semente": semente,
        "armazens": armazens,  # <- manda pro template
    }
    return render(request, "GestaoSementes/detalhes_sementes.html", contexto)

def deletar_semente(request, id):
    semente = get_object_or_404(TipoSemente, idtiposemente=id)

    # Lotes associados a essa semente
    lotes = Lote.objects.filter(tiposemente_idtiposemente=id).select_related("armazem_idarmazem")

    if request.method == "POST":
        apagar_lotes = request.POST.get("apagar_lotes") == "sim"

        # Se há lotes, só permite excluir se o usuário optar por excluir os lotes também
        if lotes.exists():
            if not apagar_lotes:
                messages.error(
                    request,
                    "Esta semente possui lotes associados. "
                    "Marque a opção para apagar também os lotes, se quiser prosseguir."
                )
                return redirect("deletar_semente", id=id)

            # Apaga todos os lotes dessa semente
            lotes.delete()

        # Agora pode apagar a semente
        semente.delete()
        messages.success(request, "Semente (e lotes associados, se houveram) deletada com sucesso!")
        return redirect("gestao_sementes")

    # GET → mostra tela de confirmação com a lista de lotes
    context = {
        "semente": semente,
        "lotes": lotes,
    }
    return render(request, "GestaoSementes/confirmar_delete_semente.html", context)

def home(request):
    return render(request, "Home/Home.html")


def perfil_gestor(request):
    # pega dados da sessão
    tipo_usuario = request.session.get("user_tipo")
    user_id = request.session.get("user_id")   # para Gestor é o CPF

    # se não estiver logado
    if not tipo_usuario or not user_id:
        messages.error(request, "Faça login para acessar seu perfil.")
        return redirect("login_view")

    # se não for gestor, bloqueia esse perfil
    if tipo_usuario != "gestor":
        messages.error(request, "Apenas gestores podem acessar essa página.")
        return redirect("home")  # ou outra página padrão

    # busca o gestor logado
    gestor = get_object_or_404(Gestor, pk=user_id)

    # telefone(s) do gestor
    telefones = Telefone.objects.filter(gestor_cpf=gestor.cpf).values_list(
        "numero", flat=True
    )
    telefone_principal = telefones[0] if telefones else None

    # armazéns sob gestão desse gestor
    armazens = Armazem.objects.filter(gestor_cpf=gestor)

    context = {
        "gestor": gestor,
        "telefone_principal": telefone_principal,
        "armazens": armazens,
    }
    return render(request, "PerfilGestor/PerfilGestor.html", context)

def editar_perfil_gestor(request):
    # garante que o usuário logado é um gestor
    if request.session.get("user_tipo") != "gestor":
        messages.error(request, "Você precisa estar logado como gestor para editar o perfil.")
        return redirect("login_view")

    cpf = request.session.get("user_id")
    gestor = get_object_or_404(Gestor, pk=cpf)

    telefone_obj = Telefone.objects.filter(gestor_cpf=gestor).first()
    telefone_atual = telefone_obj.numero if telefone_obj else ""

    if request.method == "POST":
        nome = request.POST.get("nome_completo", "").strip()
        usuario = request.POST.get("usuario", "").strip()
        email = request.POST.get("email", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        senha = request.POST.get("senha") or ""
        confirmar = request.POST.get("confirmar_senha") or ""

        erros = []

        if not nome or not usuario or not email:
            erros.append("Nome, usuário e e-mail são obrigatórios.")

        # e-mail já usado por outro gestor
        if Gestor.objects.filter(email=email).exclude(pk=gestor.cpf).exists():
            erros.append("Já existe um gestor com esse e-mail.")

        # usuário já usado por outro gestor
        if Gestor.objects.filter(usuario=usuario).exclude(pk=gestor.cpf).exists():
            erros.append("Já existe um gestor com esse usuário.")

        # validação de senha (se o usuário preencheu)
        if senha or confirmar:
            if senha != confirmar:
                erros.append("A nova senha e a confirmação não conferem.")

        if erros:
            for e in erros:
                messages.error(request, e)
            # re-renderiza com os dados atuais
            context = {
                "gestor": gestor,
                "telefone": telefone_atual,
            }
            return render(request, "PerfilGestor/editar_perfil.html", context)

        # atualiza campos básicos
        gestor.nome = nome
        gestor.usuario = usuario
        gestor.email = email

        # se o usuário informou uma nova senha, gera o hash
        if senha:
            gestor.senha_hash = make_password(senha)

        gestor.save()

        # Atualiza/cria/deleta telefone
        if telefone:
            if telefone_obj:
                telefone_obj.numero = telefone
                telefone_obj.save()
            else:
                Telefone.objects.create(
                    numero=telefone,
                    gestor_cpf=gestor
                )
        else:
            # se esvaziou o telefone e existia um, apaga
            if telefone_obj:
                telefone_obj.delete()

        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("perfil_gestor")

    # GET: mostra o formulário preenchido
    context = {
        "gestor": gestor,
        "telefone": telefone_atual,
    }
    return render(request, "PerfilGestor/editar_perfil.html", context)


def gestao_armazens(request):
    # Busca todos os armazéns
    armazens = Armazem.objects.select_related("gestor_cpf").all()

    lista_armazens = []

    for armazem in armazens:
        # Soma dos pesos dos lotes daquele armazém
        capacidade_atual = (
            Lote.objects
            .filter(armazem_idarmazem=armazem.idarmazem)
            .aggregate(total=Sum("peso"))["total"] or 0
        )

        # Capacidade total ainda não existe no seu banco → deixo como 0
        capacidade_total = 0  

        status = "Ativo" if capacidade_atual > 0 else "Vazio"

        lista_armazens.append({
            "id": armazem.idarmazem,
            "nome": armazem.nome,
            "gestor": armazem.gestor_cpf,
            "capacidade_atual": capacidade_atual,
            "capacidade_total": capacidade_total,
            "status": status,
        })

    context = {
        "armazens": lista_armazens
    }

    return render(request, "GestaoArmazens/GestaoArmazens.html", context)

def ver_armazens(request, armazem_id):
    
    armazem = get_object_or_404(
        Armazem.objects.select_related(
            "gestor_cpf",          
            "endereco_idendereco", 
            "operadorarmazem_idoperadorarmazem"  
        ),
        pk=armazem_id
    )

    
    lotes = (
        Lote.objects
        .filter(armazem_idarmazem=armazem)   
        .order_by("-dataentrada")           
    )


    tipos_sementes = (
        TipoSemente.objects
        .filter(lote__armazem_idarmazem=armazem)
        .distinct()
    )

    context = {
        "armazem": armazem,
        "lotes": lotes,
        "tipos_sementes": tipos_sementes,
    }

    return render(request, "GestaoArmazens/VerArmazens.html", context)


def cadastrar_armazens(request):
    # garante que é gestor logado
    if request.session.get("user_tipo") != "gestor":
        messages.error(request, "Você precisa estar logado como gestor para cadastrar armazéns.")
        return redirect("login_view")

    cpf = request.session.get("user_id")
    gestor = Gestor.objects.filter(cpf=cpf).first()
    if not gestor:
        messages.error(request, "Gestor não encontrado. Faça login novamente.")
        return redirect("login_view")

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        # endereço
        rua   = request.POST.get("rua", "").strip()
        numero = request.POST.get("numero", "").strip()
        bairro = request.POST.get("bairro", "").strip()
        cidade = request.POST.get("cidade", "").strip()
        uf     = request.POST.get("uf", "").strip()
        cep    = request.POST.get("cep", "").strip()
        comp   = request.POST.get("comp", "").strip()

        # operador (opcional)
        operador_id = request.POST.get("operador_id", "").strip()

        erros = []

        if not nome:
            erros.append("O nome do armazém é obrigatório.")

        # valida campos de endereço
        if not rua or not numero or not bairro or not cidade or not uf or not cep:
            erros.append("Preencha todos os campos obrigatórios de endereço.")

        # número
        try:
            numero_int = int(numero)
        except ValueError:
            erros.append("Número do endereço inválido.")
            numero_int = None

        # UF com 2 letras
        if uf and len(uf) != 2:
            erros.append("UF deve ter exatamente 2 letras.")

        # valida operador se vier preenchido
        operador = None
        if operador_id:
            try:
                operador = OperadorArmazem.objects.get(idoperadorarmazem=int(operador_id))
            except (ValueError, OperadorArmazem.DoesNotExist):
                erros.append("Operador de armazém selecionado é inválido.")

        if erros:
            for e in erros:
                messages.error(request, e)

            operadores = OperadorArmazem.objects.all()
            context = {
                "gestor": gestor,
                "operadores": operadores,
                # se quiser, dá pra mandar os dados de volta pra repovoar os campos
            }
            return render(request, "GestaoArmazens/CadastrarArmazens.html", context)

        # cria endereço
        endereco = Endereco.objects.create(
            uf=uf.upper(),
            cidade=cidade,
            bairro=bairro,
            rua=rua,
            numero=numero_int,
            comp=comp or None,
            cep=cep,
        )

        # cria armazém
        Armazem.objects.create(
            nome=nome,
            descricao=descricao,
            gestor_cpf=gestor,                      # FK pelo objeto
            endereco_idendereco=endereco,          # FK pelo objeto
            operadorarmazem_idoperadorarmazem=operador  # pode ser None
        )

        messages.success(request, "Armazém cadastrado com sucesso!")
        return redirect("gestao_armazens")

    # GET → mostra formulário
    operadores = OperadorArmazem.objects.all()
    context = {
        "gestor": gestor,
        "operadores": operadores,
    }
    return render(request, "GestaoArmazens/CadastrarArmazens.html", context)


def editar_armazem(request, id):
    # busca o armazém com as FKs necessárias
    armazem = get_object_or_404(
        Armazem.objects.select_related(
            "gestor_cpf",
            "endereco_idendereco",
            "operadorarmazem_idoperadorarmazem",
        ),
        pk=id,
    )

    endereco = armazem.endereco_idendereco
    operadores = OperadorArmazem.objects.all()

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        descricao = request.POST.get("descricao", "").strip()

        # endereço
        rua = request.POST.get("rua", "").strip()
        numero = request.POST.get("numero", "").strip()
        bairro = request.POST.get("bairro", "").strip()
        cidade = request.POST.get("cidade", "").strip()
        uf = request.POST.get("uf", "").strip()
        cep = request.POST.get("cep", "").strip()
        comp = request.POST.get("comp", "").strip()

        # operador (opcional)
        operador_id = request.POST.get("operador_id", "").strip()

        erros = []

        if not nome:
            erros.append("O nome do armazém é obrigatório.")

        if not rua or not numero or not bairro or not cidade or not uf or not cep:
            erros.append("Preencha todos os campos obrigatórios de endereço.")

        try:
            numero_int = int(numero)
        except ValueError:
            erros.append("Número do endereço inválido.")
            numero_int = None

        if uf and len(uf) != 2:
            erros.append("UF deve ter exatamente 2 letras.")

        operador = None
        if operador_id:
            try:
                operador = OperadorArmazem.objects.get(
                    idoperadorarmazem=int(operador_id)
                )
            except (ValueError, OperadorArmazem.DoesNotExist):
                erros.append("Operador de armazém selecionado é inválido.")

        if erros:
            for e in erros:
                messages.error(request, e)

            context = {
                "armazem": armazem,
                "endereco": endereco,
                "operadores": operadores,
            }
            return render(request, "GestaoArmazens/editar_armazem.html", context)

        # Atualiza endereço existente
        endereco.rua = rua
        endereco.numero = numero_int
        endereco.bairro = bairro
        endereco.cidade = cidade
        endereco.uf = uf.upper()
        endereco.cep = cep
        endereco.comp = comp or None
        endereco.save()

        # Atualiza armazém
        armazem.nome = nome
        armazem.descricao = descricao
        armazem.operadorarmazem_idoperadorarmazem = operador  # pode ser None
        armazem.save()

        messages.success(request, "Armazém atualizado com sucesso!")
        return redirect("ver_armazens", armazem_id=armazem.idarmazem)

    # GET → mostra o formulário preenchido
    context = {
        "armazem": armazem,
        "endereco": endereco,
        "operadores": operadores,
    }
    return render(request, "GestaoArmazens/editar_armazem.html", context)

def deletar_armazem(request, armazem_id):

    armazem = get_object_or_404(
        Armazem.objects.select_related("endereco_idendereco", "gestor_cpf"),
        pk=armazem_id
    )

    lotes = Lote.objects.filter(armazem_idarmazem=armazem)

    # -------- GET → mostrar tela de confirmação --------
    if request.method == "GET":
        return render(
            request,
            "GestaoArmazens/ConfirmarDelete.html",
            {"armazem": armazem, "lotes": lotes},
        )

    # -------- POST → tentativa de exclusão --------
    apagar_lotes = request.POST.get("apagar_lotes")

    # se tem lotes e usuário NÃO marcou "apagar lotes"
    if lotes.exists() and not apagar_lotes:
        messages.error(
            request,
            "Este armazém possui lotes associados. Confirme se deseja apagá-los."
        )
        return render(
            request,
            "GestaoArmazens/ConfirmarDelete.html",
            {"armazem": armazem, "lotes": lotes},
        )

    # se usuário confirmar apagar lotes
    if apagar_lotes:
        lotes.delete()

    # agora pode excluir o armazém
    armazem.delete()

    messages.success(request, "Armazém deletado com sucesso!")
    return redirect("gestao_armazens")


def gestao_lotes(request):
    return render(request,"GestaoLotes/GestaoLotes.html")


def cadastrar_lotes(request):
    return render(request,"GestaoLotes/CadastrarLotes.html")


def dashboard(request):
    return render(request,"Dashboard/Dashboard.html")

def cadastro_solicitacoes(request):
    return render(request,"GestaoSolicitacoes/CadastroSolicitacoes.html")

def gestao_solicitacoes(request):
    return render(request,"GestaoSolicitacoes/GestaoSolicitacoes.html")