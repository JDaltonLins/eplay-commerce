from django import forms
from manager.models.usuario import Usuario

class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    remeber = forms.BooleanField(required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'password']

class RegistrarForm(forms.ModelForm):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', max_length=100)
    password2 = forms.CharField(label='Confirmar senha', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    first_name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)

    class Meta:
        model = Usuario
        fields = ['username', 'password']