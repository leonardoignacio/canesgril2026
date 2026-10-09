from django.urls import path
from usuarios.views import (
    cadastro, login_view, dashboard, logout_view, 
    cria_prato, edita_prato, atualiza_prato, deleta_prato,
    edita_perfil, altera_senha # Novas importações
)

app_name = 'usuarios'

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'), 
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'), 
    path('logout/', logout_view, name='logout'),
    path('cria-prato/', cria_prato, name='cria_prato'),
    path('deleta/<int:prato_id>/', deleta_prato, name='deleta_prato'),
    path('edita/<int:prato_id>/', edita_prato, name='edita_prato'),
    path('atualiza-prato/', atualiza_prato, name='atualiza_prato'),
    
    # NOVAS ROTAS: Controle de Perfil do Usuário
    path('perfil/editar/', edita_perfil, name='edita_perfil'),
    path('perfil/senha/', altera_senha, name='altera_senha'),
]