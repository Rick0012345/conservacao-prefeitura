from django.contrib import admin
from .models import Relatorio, ImagemRelatorio

class ImagemRelatorioInline(admin.TabularInline):
    """Inline para gerenciar imagens dentro do relatório"""
    model = ImagemRelatorio
    extra = 1
    fields = ['imagem', 'legenda', 'ordem']
    readonly_fields = ['data_upload']

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'data_criacao', 'get_imagens_count']
    list_filter = ['data_criacao', 'usuario']
    search_fields = ['titulo', 'conteudo', 'usuario__username']
    readonly_fields = ['data_criacao']
    ordering = ['-data_criacao']
    inlines = [ImagemRelatorioInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')
    
    def get_imagens_count(self, obj):
        """Retorna o número de imagens do relatório"""
        return obj.imagens.count()
    get_imagens_count.short_description = 'Imagens'

@admin.register(ImagemRelatorio)
class ImagemRelatorioAdmin(admin.ModelAdmin):
    list_display = ['relatorio', 'imagem', 'legenda', 'ordem', 'data_upload']
    list_filter = ['data_upload', 'relatorio__usuario']
    search_fields = ['relatorio__titulo', 'legenda']
    readonly_fields = ['data_upload']
    ordering = ['relatorio', 'ordem', 'data_upload']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('relatorio')
