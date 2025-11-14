# apps/index/admin.py
from django.contrib import admin
from .models import (
    Gestor, Endereco, OperadorArmazem, Armazem, Cooperativa, Telefone,
    TipoSemente, Lote, Safra, Status, Solicitacao, SolicitacaoTipoSemente
)

# ===== Helpers =====
class BaseReadOnlyPKAdmin(admin.ModelAdmin):
    readonly_fields = ()  # você pode adicionar PK aqui se quiser travar edição da PK no admin

# ===== Cadastros básicos =====
@admin.register(Gestor)
class GestorAdmin(BaseReadOnlyPKAdmin):
    list_display = ('cpf', 'nome', 'email', 'senha_hash', 'usuario')
    search_fields = ('cpf', 'nome', 'email')
    ordering = ('nome',)

@admin.register(Endereco)
class EnderecoAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idendereco', 'uf', 'cidade', 'bairro', 'rua', 'numero', 'cep')
    search_fields = ('cidade', 'bairro', 'rua', 'cep')
    list_filter = ('uf', 'cidade')
    ordering = ('cidade', 'bairro', 'rua')

@admin.register(OperadorArmazem)
class OperadorArmazemAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idoperadorarmazem', 'nome', 'email', 'senha_hash', 'usuario')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(TipoSemente)
class TipoSementeAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idtiposemente', 'nome', 'descricao')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

@admin.register(Status)
class StatusAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idstatus', 'nome', 'descricao')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)

@admin.register(Safra)
class SafraAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idsafra', 'ano', 'descricao', 'safracol')
    search_fields = ('descricao', 'safracol')
    ordering = ('-ano',)

# ===== Entidades com FKs =====
@admin.register(Armazem)
class ArmazemAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idarmazem', 'nome', 'gestor_cpf', 'endereco_idendereco', 'operadorarmazem_idoperadorarmazem')
    search_fields = ('nome', 'descricao', 'gestor_cpf__cpf', 'gestor_cpf__nome')
    list_filter = ('gestor_cpf',)
    autocomplete_fields = ('gestor_cpf', 'endereco_idendereco', 'operadorarmazem_idoperadorarmazem')
    list_select_related = ('gestor_cpf', 'endereco_idendereco', 'operadorarmazem_idoperadorarmazem')
    ordering = ('nome',)

@admin.register(Cooperativa)
class CooperativaAdmin(BaseReadOnlyPKAdmin):
    list_display = ('cnpj', 'razaosocial', 'nomeresponsavel', 'emailinstitucional', 'endereco_idendereco', 'senha_hash', 'usuario')
    search_fields = ('cnpj', 'razaosocial', 'nomeresponsavel', 'emailinstitucional')
    autocomplete_fields = ('endereco_idendereco',)
    list_select_related = ('endereco_idendereco',)
    ordering = ('razaosocial',)

@admin.register(Telefone)
class TelefoneAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idtelefone', 'numero', 'gestor_cpf', 'cooperativa_cnpj')
    search_fields = ('numero', 'gestor_cpf__cpf', 'gestor_cpf__nome', 'cooperativa_cnpj__cnpj', 'cooperativa_cnpj__razaosocial')
    autocomplete_fields = ('gestor_cpf', 'cooperativa_cnpj')
    list_select_related = ('gestor_cpf', 'cooperativa_cnpj')
    ordering = ('idtelefone',)

@admin.register(Lote)
class LoteAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idlote', 'peso', 'dataentrada', 'datavencimento', 'armazem_idarmazem', 'tiposemente_idtiposemente', 'qr_payload', 'lotecol')
    search_fields = ('idlote', 'qr_payload', 'lotecol')
    list_filter = ('dataentrada', 'datavencimento', 'armazem_idarmazem', 'tiposemente_idtiposemente')
    autocomplete_fields = ('armazem_idarmazem', 'tiposemente_idtiposemente')
    list_select_related = ('armazem_idarmazem', 'tiposemente_idtiposemente')
    ordering = ('-dataentrada',)

@admin.register(Solicitacao)
class SolicitacaoAdmin(BaseReadOnlyPKAdmin):
    list_display = ('idsolicitacao', 'quantidade', 'numeroprodutoresbeneficiados', 'cooperativa_cnpj', 'safra_idsafra', 'status_idstatus', 'observacao')
    search_fields = ('idsolicitacao', 'observacao', 'cooperativa_cnpj__cnpj', 'cooperativa_cnpj__razaosocial')
    list_filter = ('status_idstatus', 'safra_idsafra')
    autocomplete_fields = ('cooperativa_cnpj', 'safra_idsafra', 'status_idstatus')
    list_select_related = ('cooperativa_cnpj', 'safra_idsafra', 'status_idstatus')
    ordering = ('-idsolicitacao',)

@admin.register(SolicitacaoTipoSemente)
class SolicitacaoTipoSementeAdmin(BaseReadOnlyPKAdmin):
    list_display = ('id', 'solicitacao_idsolicitacao', 'tiposemente_idtiposemente', 'quantidade')
    search_fields = ('solicitacao_idsolicitacao__idsolicitacao', 'tiposemente_idtiposemente__nome')
    list_filter = ('tiposemente_idtiposemente',)
    autocomplete_fields = ('solicitacao_idsolicitacao', 'tiposemente_idtiposemente')
    list_select_related = ('solicitacao_idsolicitacao', 'tiposemente_idtiposemente')
    ordering = ('id',)
