from apps.index.views import index, login_view, cadastro_cooperativa, cadastro_gestor, gestao_cooperativa,home
from django.urls import path


urlpatterns = [
        path('', index, name='index'),
        path('login_view/', login_view, name='login_view'),
        path('cadastro_cooperativa/', cadastro_cooperativa, name='cadastro_cooperativa'),
        path('cadastro_gestor/', cadastro_gestor, name='cadastro_gestor'),
        path('gestao_cooperativa/', gestao_cooperativa, name='gestao_cooperativa'),
         path('home/', home, name='home')
        
    ]   