from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Relatorio
from .forms import RelatorioForm, CustomUserCreationForm

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

@login_required
def criar_relatorio(request):
    """View para criação de relatórios por usuários normais"""
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            relatorio = form.save(commit=False)
            relatorio.usuario = request.user
            relatorio.save()
            messages.success(request, 'Relatório criado com sucesso!')
            return redirect('criar_relatorio')
    else:
        form = RelatorioForm()
    
    return render(request, 'core/criar_relatorio.html', {'form': form})

@login_required
def meus_relatorios(request):
    """View para visualização dos relatórios do usuário logado"""
    relatorios = Relatorio.objects.filter(usuario=request.user)
    
    # Paginação
    paginator = Paginator(relatorios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/meus_relatorios.html', {
        'relatorios': page_obj,
        'total_relatorios': relatorios.count()
    })

@login_required
@user_passes_test(is_admin)
def admin_relatorios(request):
    """View para admin visualizar todos os relatórios"""
    relatorios = Relatorio.objects.all()
    
    # Filtros
    search = request.GET.get('search', '')
    usuario_filtro = request.GET.get('usuario', '')
    
    if search:
        relatorios = relatorios.filter(
            Q(titulo__icontains=search) | 
            Q(conteudo__icontains=search) |
            Q(usuario__username__icontains=search)
        )
    
    if usuario_filtro:
        relatorios = relatorios.filter(usuario__username=usuario_filtro)
    
    # Paginação
    paginator = Paginator(relatorios, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Lista de usuários para filtro
    usuarios = User.objects.filter(relatorio__isnull=False).distinct()
    
    return render(request, 'core/admin_relatorios.html', {
        'relatorios': page_obj,
        'usuarios': usuarios,
        'search': search,
        'usuario_filtro': usuario_filtro,
        'total_relatorios': relatorios.count()
    })

@login_required
@user_passes_test(is_admin)
def detalhes_relatorio(request, pk):
    """View para visualizar detalhes de um relatório específico"""
    relatorio = get_object_or_404(Relatorio, pk=pk)
    return render(request, 'core/detalhes_relatorio.html', {'relatorio': relatorio})

def register(request):
    """View para registro de novos usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
