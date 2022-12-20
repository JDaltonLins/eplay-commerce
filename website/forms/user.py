from django import forms

from manager.models.usuario import Usuario


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'imagem']
