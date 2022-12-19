from django import forms
from manager.models.usuario import Usuario
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', min_length=8,  max_length=100)
    password = forms.CharField(
        label='Senha', max_length=100, min_length=8, widget=forms.PasswordInput)
    remeber = forms.BooleanField(label='Lembrar de mim', required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            'remeber',
            Submit('submit', 'Entrar', css_class='btn btn-primary')
        )


class RegistrarForm(forms.ModelForm):
    username = forms.CharField(label='Usuário', min_length=8, max_length=100)
    password = forms.CharField(
        label='Senha', max_length=100, min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar senha', max_length=100, min_length=8, widget=forms.PasswordInput)
    email = forms.CharField(label='Email', max_length=100)
    first_name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)

    def __init__(self, *args, **kwargs):
        super(RegistrarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name',
            Submit('submit', 'Registrar', css_class='btn btn-primary')
        )

    def clean(self):
        data = super().clean()

        if data['password'] != data['password2']:
            self.add_error('password', 'As senhas não conferem')
            self.add_error('password2', 'As senhas não conferem')

    class Meta:
        model = Usuario
        fields = ['username', 'password',
                  'first_name', 'last_name', 'email']


class ChangeEmailForm(forms.Form):
    email = forms.CharField(
        max_length=120, label='Novo email', required=True, widget=forms.EmailInput)
    confirm_email = forms.CharField(
        max_length=120, label='Confirmar email', required=True, widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'confirm_email',
            Submit('submit', 'Alterar', css_class='btn btn-primary')
        )

    def clean(self):
        data = super().clean()

        if data['email'] != data['confirm_email']:
            self.add_error('email', 'Os emails não conferem')
            self.add_error('confirm_email', 'Os emails não conferem')

        return data
