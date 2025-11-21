from apps.index.views import (
    index, login_view, cadastro_cooperativa, cadastro_gestor, 
    gestao_cooperativas,home, editar_cooperativa, detalhe_cooperativa,
    gestao_sementes, cadastrar_semente,editar_semente, detalhes_semente,gestao_sementes2, perfil_gestor,
    gestao_armazens,ver_armazens,cadastrar_armazens,gestao_lotes,cadastrar_lotes)
from django.urls import path


urlpatterns = [
        path('', index, name='index'),
        path('login_view/', login_view, name='login_view'),
        path('cadastro_cooperativa/', cadastro_cooperativa, name='cadastro_cooperativa'),
        path("cooperativas/<path:cnpj>/editar/", editar_cooperativa, name="editar_cooperativa"),
        path('cadastro_gestor/', cadastro_gestor, name='cadastro_gestor'),
        path('gestao_cooperativa/', gestao_cooperativas, name='gestao_cooperativa'),
        path('home/', home, name='home'),
        path("detalhescooperativas/<path:cnpj>/", detalhe_cooperativa, name="detalhe_cooperativa"),
        path('gestao_sementes/', gestao_sementes, name='gestao_sementes'),
        path('cadastrar_sementes/', cadastrar_semente, name='cadastrar_semente'),
        path("sementes/<path:id>/editar/", editar_semente, name="editar_semente"),
        path("sementes/<int:id>/detalhes/", detalhes_semente, name="detalhes_semente"),
         path('gestao_sementes2/', gestao_sementes2, name='gestao_sementes2'),
        path("perfil_gestor/",perfil_gestor, name='perfil_gestor'),
        path("gestao_armazens/",gestao_armazens, name='gestao_armazens'),
        path("ver-armazens/<int:armazem_id>/", ver_armazens, name='ver_armazens'),
        path("cadastrar_armazens/",cadastrar_armazens, name='cadastrar_armazens'),
        path("gestao_lotes/",gestao_lotes, name='gestao_lotes'),
        path("cadastrar_lotes/",cadastrar_lotes, name='cadastrar_lotes')
    ]   