from django.urls import path
from .views import *
urlpatterns = [
    path('cadastro', cadastro, name='cadastro'), 
    path('login', login, name='login'),
    path('dashboard', dashboard, name='dashboard'), 
    path('logout', logout, name='logout'),
    path('cria-prato', cria_prato, name='cria_prato'),
    path('deleta/<int:prato_id>', deleta_prato, name='deleta_prato'),
    path('edita/<int:prato_id>', edita_prato, name='edita_prato'),
    path('atualiza_prato', atualiza_prato, name='atualiza_prato')
]