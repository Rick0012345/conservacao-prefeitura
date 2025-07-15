from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from .models import Relatorio, ImagemRelatorio
import os

class MultipleFileInput(forms.ClearableFileInput):
    """Widget personalizado para upload múltiplo de arquivos"""
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    """Campo personalizado para upload múltiplo de arquivos"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Se for uma lista de arquivos, processar cada um
        if isinstance(data, list):
            result = []
            for file in data:
                result.append(super().clean(file, initial))
            return result
        return super().clean(data, initial)

class RelatorioForm(forms.ModelForm):
    """Formulário para criação de relatórios"""
    
    nome_usuario = forms.CharField(
        max_length=100,
        required=False,
        label="Seu nome",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo'
        })
    )
    
    email_usuario = forms.EmailField(
        required=False,
        label="Seu email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )
    
    class Meta:
        model = Relatorio
        fields = ['titulo', 'conteudo', 'nome_usuario', 'email_usuario']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do relatório'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Descreva detalhadamente o problema ou situação...'
            }),
        }
        labels = {
            'titulo': 'Título do Relatório',
            'conteudo': 'Descrição do Problema'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Se o usuário estiver logado, remover campos de nome e email
        if self.user and self.user.is_authenticated:
            self.fields.pop('nome_usuario', None)
            self.fields.pop('email_usuario', None)
        else:
            # Se não estiver logado, tornar obrigatórios os campos de nome e email
            self.fields['nome_usuario'].required = True
            self.fields['email_usuario'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar se usuário não logado preencheu nome e email
        if not (self.user and self.user.is_authenticated):
            if not cleaned_data.get('nome_usuario'):
                self.add_error('nome_usuario', 'Este campo é obrigatório.')
            if not cleaned_data.get('email_usuario'):
                self.add_error('email_usuario', 'Este campo é obrigatório.')
        
        return cleaned_data

class ImagemRelatorioForm(forms.ModelForm):
    """Formulário para upload de imagens de relatórios"""
    
    class Meta:
        model = ImagemRelatorio
        fields = ['imagem', 'legenda']
        widgets = {
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'legenda': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da imagem (opcional)'
            })
        }
        labels = {
            'imagem': 'Imagem',
            'legenda': 'Legenda'
        }
    
    def clean_imagem(self):
        """Validação personalizada para o campo imagem"""
        from django.conf import settings
        import os
        
        imagem = self.cleaned_data.get('imagem')
        
        if imagem:
            # Verifica o tamanho do arquivo
            if imagem.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    f'O arquivo é muito grande. Tamanho máximo permitido: {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB'
                )
            
            # Verifica o tipo do arquivo
            if hasattr(imagem, 'content_type'):
                if imagem.content_type not in settings.ALLOWED_IMAGE_TYPES:
                    raise forms.ValidationError(
                        'Tipo de arquivo não suportado. Use apenas JPG, PNG ou GIF.'
                    )
            
            # Verifica a extensão do arquivo
            ext = os.path.splitext(imagem.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                raise forms.ValidationError(
                    'Extensão de arquivo não suportada. Use apenas .jpg, .jpeg, .png ou .gif.'
                )
        
        return imagem

# Formset para múltiplas imagens
ImagemRelatorioFormSet = modelformset_factory(
    ImagemRelatorio,
    form=ImagemRelatorioForm,
    extra=3,  # Número de formulários vazios adicionais
    can_delete=True,
    fields=['imagem', 'legenda']
)

class MultipleImageUploadForm(forms.Form):
    """Formulário para upload múltiplo de imagens"""
    imagens = MultipleFileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True
        }),
        label='Imagens',
        help_text='Você pode selecionar múltiplas imagens de uma vez',
        required=False
    )
    
    def clean_imagens(self):
        """Validação para múltiplas imagens"""
        from django.conf import settings
        import os
        
        images = self.files.getlist('imagens')
        
        if images:
            for image in images:
                # Verifica o tamanho do arquivo
                if image.size > settings.MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(
                        f'Arquivo {image.name} é muito grande. Tamanho máximo: {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB'
                    )
                
                # Verifica o tipo do arquivo
                if hasattr(image, 'content_type'):
                    if image.content_type not in settings.ALLOWED_IMAGE_TYPES:
                        raise forms.ValidationError(
                            f'Arquivo {image.name} não é suportado. Use apenas JPG, PNG ou GIF.'
                        )
                
                # Verifica a extensão do arquivo
                ext = os.path.splitext(image.name)[1].lower()
                if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                    raise forms.ValidationError(
                        f'Extensão de {image.name} não suportada. Use apenas .jpg, .jpeg, .png ou .gif.'
                    )
        
        return images

class CustomUserCreationForm(UserCreationForm):
    """Formulário personalizado para criação de usuários"""
    
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 