from django.urls import path
from . import views


app_name = 'core'
urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    
    # Autenticação
    path('register/', views.register, name='register'),
    
    # Relatórios - Usuários
    path('relatorios/criar/', views.criar_relatorio, name='criar_relatorio'),
    path('relatorios/meus/', views.meus_relatorios, name='meus_relatorios'),
    path('relatorios/<int:pk>/', views.detalhes_relatorio_publico, name='detalhes_relatorio_publico'),
    
    # Relatórios - Admin
    path('admin/relatorios/', views.admin_relatorios, name='admin_relatorios'),
    path('admin/relatorios/<int:pk>/', views.detalhes_relatorio, name='detalhes_relatorio'),
] 