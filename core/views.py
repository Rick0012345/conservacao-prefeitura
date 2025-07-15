from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from .models import Relatorio, ImagemRelatorio
from .forms import RelatorioForm, CustomUserCreationForm, MultipleImageUploadForm

# Create your views here.

def home(request):
    """View para a página inicial"""
    return render(request, 'core/home.html')

def sobre(request):
    """View para a página sobre"""
    return render(request, 'core/sobre.html')

def contato(request):
    """View para a página de contato"""
    return render(request, 'core/contato.html')

def is_admin(user):
    """Função para verificar se o usuário é admin"""
    return user.is_staff or user.is_superuser

def criar_relatorio(request):
    """View para criação de relatórios - disponível apenas para usuários comuns"""
    # Bloquear acesso para administradores
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, 'Administradores não podem criar relatórios. Use o painel administrativo para visualizar relatórios.')
        return redirect('core:admin_relatorios')
    
    if request.method == 'POST':
        form = RelatorioForm(request.POST, user=request.user)
        image_form = MultipleImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and image_form.is_valid():
            try:
                with transaction.atomic():
                    # Criar o relatório
                    relatorio = form.save(commit=False)
                    
                    # Se o usuário estiver logado, associar ao relatório
                    if request.user.is_authenticated:
                        relatorio.usuario = request.user
                    
                    relatorio.save()
                    
                    # Processar imagens se houver
                    imagens = image_form.cleaned_data.get('imagens', [])
                    if imagens:
                        for ordem, imagem in enumerate(imagens):
                            ImagemRelatorio.objects.create(
                                relatorio=relatorio,
                                imagem=imagem,
                                ordem=ordem
                            )
                    
                    messages.success(request, 'Relatório criado com sucesso!')
                    
                    # Armazenar ID do relatório na sessão para usuários anônimos
                    if not request.user.is_authenticated:
                        relatorios_sessao = request.session.get('relatorios_criados', [])
                        relatorios_sessao.append(relatorio.id)
                        request.session['relatorios_criados'] = relatorios_sessao
                    
                    return redirect('core:criar_relatorio')
            
            except Exception as e:
                messages.error(request, f'Erro ao criar relatório: {str(e)}')
    else:
        form = RelatorioForm(user=request.user)
        image_form = MultipleImageUploadForm()
    
    return render(request, 'core/criar_relatorio.html', {
        'form': form,
        'image_form': image_form
    })

def meus_relatorios(request):
    """View para visualização dos relatórios do usuário - disponível apenas para usuários comuns"""
    # Bloquear acesso para administradores
    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, 'Administradores não possuem relatórios próprios. Use o painel administrativo para visualizar todos os relatórios.')
        return redirect('core:admin_relatorios')
    
    if request.user.is_authenticated:
        # Usuário logado: mostrar relatórios do usuário
        relatorios = Relatorio.objects.filter(usuario=request.user).prefetch_related('imagens_relatorio')
        titulo_pagina = f"Meus Relatórios ({request.user.username})"
    else:
        # Usuário anônimo: mostrar relatórios da sessão
        relatorios_ids = request.session.get('relatorios_criados', [])
        relatorios = Relatorio.objects.filter(id__in=relatorios_ids).prefetch_related('imagens_relatorio')
        titulo_pagina = "Relatórios Criados Nesta Sessão"
    
    # Paginação
    paginator = Paginator(relatorios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/meus_relatorios.html', {
        'relatorios': page_obj,
        'total_relatorios': relatorios.count(),
        'titulo_pagina': titulo_pagina
    })

def detalhes_relatorio_publico(request, pk):
    """View para visualizar detalhes de um relatório específico - para usuários comuns"""
    # Bloquear acesso para administradores (eles devem usar a view de admin)
    if request.user.is_authenticated and request.user.is_staff:
        messages.info(request, 'Redirecionando para o painel administrativo.')
        return redirect('core:detalhes_relatorio', pk=pk)
    
    relatorio = get_object_or_404(
        Relatorio.objects.prefetch_related('imagens_relatorio'),
        pk=pk
    )
    
    # Verificar se o usuário tem permissão para ver este relatório
    pode_ver = False
    
    if request.user.is_authenticated:
        # Usuário logado pode ver seus próprios relatórios
        if relatorio.usuario == request.user:
            pode_ver = True
    else:
        # Usuário anônimo pode ver apenas relatórios da sua sessão
        relatorios_ids = request.session.get('relatorios_criados', [])
        if relatorio.id in relatorios_ids:
            pode_ver = True
    
    if not pode_ver:
        messages.error(request, 'Você não tem permissão para ver este relatório.')
        return redirect('core:home')
    
    return render(request, 'core/detalhes_relatorio_publico.html', {
        'relatorio': relatorio
    })

@login_required
@user_passes_test(is_admin)
def admin_relatorios(request):
    """View para admin visualizar todos os relatórios"""
    relatorios = Relatorio.objects.all().select_related('usuario').prefetch_related('imagens_relatorio')
    
    # Filtros
    search = request.GET.get('search', '')
    usuario_filtro = request.GET.get('usuario', '')
    
    if search:
        relatorios = relatorios.filter(
            Q(titulo__icontains=search) | 
            Q(conteudo__icontains=search) |
            Q(usuario__username__icontains=search) |
            Q(nome_usuario__icontains=search) |
            Q(email_usuario__icontains=search)
        )
    
    if usuario_filtro:
        relatorios = relatorios.filter(
            Q(usuario__username=usuario_filtro) | 
            Q(nome_usuario=usuario_filtro)
        )
    
    # Paginação
    paginator = Paginator(relatorios, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Lista de usuários para filtro (incluindo anônimos)
    usuarios_logados = User.objects.filter(relatorio__isnull=False).distinct()
    usuarios_anonimos = Relatorio.objects.filter(usuario__isnull=True).exclude(nome_usuario='').values_list('nome_usuario', flat=True).distinct()
    
    # Contagem de relatórios com localização
    relatorios_com_localizacao = Relatorio.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    ).count()
    
    return render(request, 'core/admin_relatorios.html', {
        'relatorios': page_obj,
        'usuarios_logados': usuarios_logados,
        'usuarios_anonimos': usuarios_anonimos,
        'search': search,
        'usuario_filtro': usuario_filtro,
        'total_relatorios': relatorios.count(),
        'relatorios_com_localizacao': relatorios_com_localizacao
    })

@login_required
@user_passes_test(is_admin)
def detalhes_relatorio(request, pk):
    """View para visualizar detalhes de um relatório específico - apenas para admins"""
    relatorio = get_object_or_404(
        Relatorio.objects.prefetch_related('imagens_relatorio'),
        pk=pk
    )
    return render(request, 'core/detalhes_relatorio.html', {'relatorio': relatorio})

def register(request):
    """View para registro de novos usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
