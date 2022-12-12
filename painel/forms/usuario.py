from django import forms

class CadastrarUsuario(forms.ModelForm)


    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'imagem']