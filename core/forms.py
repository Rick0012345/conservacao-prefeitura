from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Relatorio, ImagemRelatorio
import os

class RelatorioForm(forms.ModelForm):
    """Formulário para criação de relatórios"""
    
    class Meta:
        model = Relatorio
        fields = ['titulo', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do relatório'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Digite o conteúdo do relatório'
            })
        }
        labels = {
            'titulo': 'Título do Relatório',
            'conteudo': 'Conteúdo do Relatório'
        }

class ImagemRelatorioForm(forms.ModelForm):
    """Formulário para upload de imagens de relatórios"""
    
    class Meta:
        model = ImagemRelatorio
        fields = ['imagem', 'legenda', 'ordem']
        widgets = {
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'multiple': True
            }),
            'legenda': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da imagem (opcional)'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Ordem de exibição'
            })
        }
        labels = {
            'imagem': 'Imagem',
            'legenda': 'Legenda',
            'ordem': 'Ordem'
        }
    
    def clean_imagem(self):
        """Validação personalizada para o campo imagem"""
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

class MultipleImagemRelatorioForm(forms.Form):
    """Formulário para upload múltiplo de imagens"""
    
    imagens = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True
        }),
        label='Selecionar Imagens',
        help_text='Você pode selecionar múltiplas imagens. Formatos: JPG, PNG, GIF. Máximo 5MB cada.'
    )
    
    def clean_imagens(self):
        """Validação para múltiplas imagens"""
        imagens = self.files.getlist('imagens')
        
        if not imagens:
            raise forms.ValidationError('Selecione pelo menos uma imagem.')
        
        for imagem in imagens:
            # Verifica o tamanho do arquivo
            if imagem.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    f'A imagem "{imagem.name}" é muito grande. Tamanho máximo: {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB'
                )
            
            # Verifica o tipo do arquivo
            if hasattr(imagem, 'content_type'):
                if imagem.content_type not in settings.ALLOWED_IMAGE_TYPES:
                    raise forms.ValidationError(
                        f'A imagem "{imagem.name}" tem tipo não suportado. Use apenas JPG, PNG ou GIF.'
                    )
            
            # Verifica a extensão do arquivo
            ext = os.path.splitext(imagem.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                raise forms.ValidationError(
                    f'A imagem "{imagem.name}" tem extensão não suportada. Use apenas .jpg, .jpeg, .png ou .gif.'
                )
        
        return imagens

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