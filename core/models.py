from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

# Create your models here.

class Relatorio(models.Model):
    """Modelo para relatórios criados pelos usuários"""
    
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Usuário",
        null=True,
        blank=True,
        help_text="Usuário logado que criou o relatório"
    )
    
    # Campos para usuários anônimos
    nome_usuario = models.CharField(
        max_length=100, 
        verbose_name="Nome do Usuário",
        blank=True,
        help_text="Nome do usuário quando não logado"
    )
    email_usuario = models.EmailField(
        verbose_name="Email do Usuário",
        blank=True,
        help_text="Email do usuário quando não logado"
    )
    
    titulo = models.CharField(
        max_length=200, 
        verbose_name="Título"
    )
    conteudo = models.TextField(
        verbose_name="Conteúdo"
    )
    data_criacao = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        ordering = ['-data_criacao']

    def __str__(self):
        if self.usuario:
            return f"{self.titulo} - {self.usuario.username}"
        elif self.nome_usuario:
            return f"{self.titulo} - {self.nome_usuario}"
        else:
            return f"{self.titulo} - Anônimo"
    
    @property
    def nome_autor(self):
        """Retorna o nome do autor do relatório"""
        if self.usuario:
            return self.usuario.username
        elif self.nome_usuario:
            return self.nome_usuario
        else:
            return "Anônimo"
    
    @property
    def email_autor(self):
        """Retorna o email do autor do relatório"""
        if self.usuario:
            return self.usuario.email
        elif self.email_usuario:
            return self.email_usuario
        else:
            return ""

    @property
    def imagens(self):
        """Retorna todas as imagens associadas ao relatório"""
        return self.imagens_relatorio.all()

def relatorio_imagem_path(instance, filename):
    """Função para definir o caminho das imagens dos relatórios"""
    # Organiza as imagens por relatório: media/relatorios/{relatorio_id}/{filename}
    return f'relatorios/{instance.relatorio.id}/{filename}'

class ImagemRelatorio(models.Model):
    """Modelo para imagens associadas aos relatórios"""
    
    relatorio = models.ForeignKey(
        Relatorio,
        on_delete=models.CASCADE,
        related_name='imagens_relatorio',
        verbose_name="Relatório"
    )
    imagem = models.ImageField(
        upload_to=relatorio_imagem_path,
        verbose_name="Imagem",
        help_text="Formatos suportados: JPG, PNG, GIF. Tamanho máximo: 5MB"
    )
    legenda = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Legenda",
        help_text="Descrição opcional da imagem"
    )
    data_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data do Upload"
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem",
        help_text="Ordem de exibição da imagem no relatório"
    )
    
    class Meta:
        verbose_name = "Imagem do Relatório"
        verbose_name_plural = "Imagens dos Relatórios"
        ordering = ['ordem', 'data_upload']
    
    def __str__(self):
        return f"Imagem {self.ordem} - {self.relatorio.titulo}"
    
    def delete(self, *args, **kwargs):
        # Remove o arquivo físico quando o objeto é deletado
        if self.imagem:
            if os.path.isfile(self.imagem.path):
                os.remove(self.imagem.path)
        super().delete(*args, **kwargs)
