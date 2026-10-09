from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from churras.models import Prato

def cadastro(request: HttpRequest) -> HttpResponse:
    """Processa o registro de novos usuários aplicando Guard Clauses."""
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('password')
        senha2 = request.POST.get('password2')

        if not nome or not email:
            messages.error(request, 'Nome e e-mail são obrigatórios.')
            return redirect('usuarios:cadastro')
        if senha != senha2:
            messages.error(request, 'As senhas não conferem.')
            return redirect('usuarios:cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado com este email.')
            return redirect('usuarios:cadastro')

        User.objects.create_user(username=nome, email=email, password=senha)
        messages.success(request, 'Cadastro realizado com sucesso.')
        return redirect('usuarios:login')

    # ALTERADO: Apontando para o form unificado (is_edit implicitamente False)
    return render(request, 'frm_usuario.html')

def login_view(request: HttpRequest) -> HttpResponse:
    """Autentica o usuário na plataforma de forma segura."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha')

        if not email or not senha:
            messages.error(request, 'Preencha e-mail e senha.')
            return redirect('usuarios:login')

        user_obj = User.objects.filter(email=email).first()
        if user_obj:
            user = auth.authenticate(request, username=user_obj.username, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('usuarios:dashboard')

        messages.error(request, 'Credenciais inválidas.')
        return redirect('usuarios:login')

    return render(request, 'login.html')

@login_required(login_url='usuarios:login')
def logout_view(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('churras:index')

@login_required(login_url='usuarios:login')
def dashboard(request: HttpRequest) -> HttpResponse:
    """Exibe apenas os pratos pertencentes ao usuário autenticado."""
    pratos = Prato.objects.filter(funcionario=request.user).order_by('-date_prato')
    paginator = Paginator(pratos, 6)
    page = request.GET.get('page')
    pratos_por_pagina = paginator.get_page(page)
    
    return render(request, 'dashboard.html', {'lista_pratos': pratos_por_pagina})

# ==========================================
# NOVOS CONTROLADORES: PERFIL DE USUÁRIO
# ==========================================

@login_required(login_url='usuarios:login')
def edita_perfil(request: HttpRequest) -> HttpResponse:
    """Atualiza dados cadastrais (Nome/Email) do usuário logado."""
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()

        if not nome or not email:
            messages.error(request, 'Nome e e-mail não podem ficar em branco.')
            return redirect('usuarios:edita_perfil')

        # Verifica se o email já existe em OUTRO usuário
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, 'Este e-mail já está sendo usado por outra conta.')
            return redirect('usuarios:edita_perfil')

        request.user.username = nome
        request.user.email = email
        request.user.save()
        
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('usuarios:dashboard')

    # Injeta a variável de controle is_edit
    return render(request, 'frm_usuario.html', {'is_edit': True})

@login_required(login_url='usuarios:login')
def altera_senha(request: HttpRequest) -> HttpResponse:
    """Valida a senha antiga, atualiza para a nova e renova a sessão HTTP."""
    if request.method == 'POST':
        senha_antiga = request.POST.get('senha_antiga')
        nova_senha = request.POST.get('nova_senha')
        confirma_senha = request.POST.get('confirma_senha')

        if not request.user.check_password(senha_antiga):
            messages.error(request, 'A senha antiga informada está incorreta.')
            return redirect('usuarios:edita_perfil')
            
        if nova_senha != confirma_senha:
            messages.error(request, 'A nova senha e a confirmação não conferem.')
            return redirect('usuarios:edita_perfil')

        # Atualiza a senha no banco (aplica o Hash SHA256)
        request.user.set_password(nova_senha)
        request.user.save()
        
        # Mantém o usuário logado após a mudança de senha
        auth.update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Senha alterada com sucesso. Sessão mantida.')
        return redirect('usuarios:dashboard')
        
    return redirect('usuarios:edita_perfil')

# ==========================================
# CONTROLADORES DE PRATOS
# ==========================================

@login_required(login_url='usuarios:login')
def cria_prato(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        Prato.objects.create(
            funcionario=request.user,
            nome_prato=request.POST.get('nome_prato'),
            ingredientes=request.POST.get('ingredientes'),
            modo_preparo=request.POST.get('modo_preparo'),
            tempo_preparo=request.POST.get('tempo_preparo', 0),
            rendimento=request.POST.get('rendimento'),
            categoria=request.POST.get('categoria'),
            publicado=request.POST.get('publicado') == 'True',
            foto_prato=request.FILES.get('foto_prato')
        )
        messages.success(request, 'Prato criado com sucesso.')
        return redirect('usuarios:dashboard')
    
    return render(request, 'frm_pratos.html')

@login_required(login_url='usuarios:login')
def edita_prato(request: HttpRequest, prato_id: int) -> HttpResponse:
    prato = get_object_or_404(Prato, pk=prato_id, funcionario=request.user)
    return render(request, 'frm_pratos.html', {'prato': prato})

@login_required(login_url='usuarios:login')
def atualiza_prato(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        prato_id = request.POST.get('prato_id')
        prato = get_object_or_404(Prato, pk=prato_id, funcionario=request.user)

        prato.nome_prato = request.POST.get('nome_prato')
        prato.ingredientes = request.POST.get('ingredientes')
        prato.modo_preparo = request.POST.get('modo_preparo')
        prato.tempo_preparo = request.POST.get('tempo_preparo', 0)
        prato.rendimento = request.POST.get('rendimento')
        prato.categoria = request.POST.get('categoria')
        prato.publicado = request.POST.get('publicado') == 'True'

        if 'foto_prato' in request.FILES:
            prato.foto_prato = request.FILES['foto_prato']

        prato.save()
        messages.success(request, 'Prato atualizado com sucesso.')
        
    return redirect('usuarios:dashboard')

@login_required(login_url='usuarios:login')
def deleta_prato(request: HttpRequest, prato_id: int) -> HttpResponse:
    prato = get_object_or_404(Prato, pk=prato_id, funcionario=request.user)
    prato.delete()
    messages.success(request, 'Prato excluído com sucesso.')
    return redirect('usuarios:dashboard')