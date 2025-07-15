from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Relatorio, ImagemRelatorio

class ImagemRelatorioInline(admin.TabularInline):
    """Inline para gerenciar imagens dentro do relatório"""
    model = ImagemRelatorio
    extra = 1
    fields = ['imagem', 'legenda', 'ordem']
    readonly_fields = ['data_upload']

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'data_criacao', 'get_imagens_count', 'get_location_status']
    list_filter = ['data_criacao', 'usuario']
    search_fields = ['titulo', 'conteudo', 'usuario__username', 'endereco']
    readonly_fields = ['data_criacao', 'get_location_map']
    ordering = ['-data_criacao']
    inlines = [ImagemRelatorioInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'conteudo', 'usuario', 'data_criacao')
        }),
        ('Dados do Usuário (se não logado)', {
            'fields': ('nome_usuario', 'email_usuario'),
            'classes': ('collapse',)
        }),
        ('Localização', {
            'fields': ('endereco', 'latitude', 'longitude', 'get_location_map'),
            'classes': ('wide',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')
    
    def get_imagens_count(self, obj):
        """Retorna o número de imagens do relatório"""
        return obj.imagens.count()
    get_imagens_count.short_description = 'Imagens'
    
    def get_location_status(self, obj):
        """Retorna o status da localização do relatório"""
        if obj.tem_localizacao:
            return format_html(
                '<span style="color: green;">✓ Com localização</span>'
            )
        else:
            return format_html(
                '<span style="color: red;">✗ Sem localização</span>'
            )
    get_location_status.short_description = 'Localização'
    
    def get_location_map(self, obj):
        """Retorna o mapa HTML para visualizar a localização"""
        if obj.tem_localizacao:
            return format_html(
                '''
                <div id="map-{}" style="width: 100%; height: 300px; border: 1px solid #ccc; border-radius: 4px;"></div>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        // Carregar Leaflet se não estiver carregado
                        if (typeof L === 'undefined') {{
                            var css = document.createElement('link');
                            css.rel = 'stylesheet';
                            css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
                            document.head.appendChild(css);
                            
                            var script = document.createElement('script');
                            script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
                            script.onload = function() {{
                                initMap{obj_id}();
                            }};
                            document.head.appendChild(script);
                        }} else {{
                            initMap{obj_id}();
                        }}
                        
                        function initMap{obj_id}() {{
                            var map = L.map('map-{obj_id}').setView([{lat}, {lng}], 15);
                            
                            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                                attribution: '© OpenStreetMap contributors'
                            }}).addTo(map);
                            
                            var marker = L.marker([{lat}, {lng}]).addTo(map);
                            
                            var popupContent = '<strong>{titulo}</strong><br>{endereco}';
                            marker.bindPopup(popupContent).openPopup();
                            
                            // Redimensionar mapa após um pequeno delay
                            setTimeout(function() {{
                                map.invalidateSize();
                            }}, 100);
                        }}
                    }});
                </script>
                <div class="mt-2">
                    <strong>Coordenadas:</strong> {lat}, {lng}<br>
                    <strong>Endereço:</strong> {endereco}
                </div>
                ''',
                obj.pk,
                obj_id=obj.pk,
                lat=obj.latitude,
                lng=obj.longitude,
                titulo=obj.titulo,
                endereco=obj.endereco or 'Não informado'
            )
        else:
            return format_html(
                '<em style="color: #666;">Localização não informada para este relatório</em>'
            )
    get_location_map.short_description = 'Mapa'

@admin.register(ImagemRelatorio)
class ImagemRelatorioAdmin(admin.ModelAdmin):
    list_display = ['relatorio', 'imagem', 'legenda', 'ordem', 'data_upload']
    list_filter = ['data_upload', 'relatorio__usuario']
    search_fields = ['relatorio__titulo', 'legenda']
    readonly_fields = ['data_upload']
    ordering = ['relatorio', 'ordem', 'data_upload']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('relatorio')
