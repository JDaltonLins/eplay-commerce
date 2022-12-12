from django import forms


class LoginForm(forms.ModelForm):

    username = forms.CharField(label='Usuário', max_length=100, required=True)
    password = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']