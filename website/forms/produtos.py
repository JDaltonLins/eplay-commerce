from django import forms
from django.forms import HiddenInput, formset_factory
from django.db.models import Max
from django.db.models.functions import Length

from manager.models.produtos import Categoria, PedidoDesconto, Produto, Tag

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, HTML


class FiltroProdutos (forms.Form):
    q = forms.CharField(label='Pesquisar', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Pesquisar', 'class': 'form-control'}))
    # Categorias irá ser por ID
    categorias = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple)
    # Tags irá ser por ID/Nome
    tags = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple)
    preco_min = forms.DecimalField(
        required=False, min_value=0, step_size=0.01, widget=forms.HiddenInput())
    preco_max = forms.DecimalField(
        required=False, min_value=0, step_size=0.01, widget=forms.HiddenInput())

    order_by = forms.ChoiceField(label='Ordernar por', choices=(
        ('nome', 'Nome'),
        ('preco', 'Preço'),
        ('data_lancamento', 'Lançamento'),
    ), required=False)
    order = forms.ChoiceField(label='Ordem', choices=(
        ('desc', 'Maior para menor'),
        ('asc', 'Menor para maior'),
    ), required=False)

    pagina = forms.IntegerField(required=False, min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['categorias'].choices = [
            (c.id, c.nome) for c in Categoria.objects.filter(ativo=True, produto__isnull=False).distinct().order_by(Length('nome'))]
        self.fields['tags'].choices = [(t.id, t.nome)
                                       for t in Tag.objects.filter(ativo=True, produto__isnull=False).distinct().order_by(Length('nome'))]
        self.fields['q'].label = False

        max = Produto.objects.all().aggregate(Max('preco'))['preco__max'] or 0
        max = (max // 10 + 1) * 10

        step_calced = max / 10

        self.fields['preco_min'].widget.attrs['max'] = max
        self.fields['preco_min'].widget.attrs['step'] = step_calced
        self.fields['preco_max'].widget.attrs['max'] = max
        self.fields['preco_max'].widget.attrs['step'] = step_calced
        self.fields['preco_max'].initial = max
        self.fields['preco_min'].initial = 0

        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.field_class = 'input-group input-group-sm'
        self.helper.layout = Layout(
            Fieldset(
                'Pesquisa',
                'categorias',
                'tags',
                Div(HTML('<label class="mb-2">Preço</label>'), Div(id='preco_slide'),
                    'preco_min', 'preco_max'),
                'order_by',
                'order',
                css_class='d-flex flex-column gap-1'
            ),
            Submit('submit', 'Pesquisar'),
        )

    # Atualiza uns campos ao carregar os dados
    def load(self, data):

        return self.cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        preco_min = cleaned_data.get('preco_min')
        preco_max = cleaned_data.get('preco_max')

        # Raise on preco_min field
        if preco_min and preco_max and preco_min > preco_max:
            raise forms.ValidationError(
                'O preço mínimo não pode ser maior que o preço máximo.')

        # Raise on preco_max field
        if preco_max and preco_min and preco_max < preco_min:
            raise forms.ValidationError(
                'O preço máximo não pode ser menor que o preço mínimo.')

        return cleaned_data

    def search(self):
        produtos = Produto.objects.all()

        q = self.cleaned_data['q']
        if q:
            produtos = produtos.filter(nome__icontains=q)

        categorias = self.cleaned_data['categorias']
        if categorias:
            produtos = produtos.filter(categorias__id__in=categorias)

        tags = self.cleaned_data['tags']
        if tags:
            produtos = produtos.filter(tags__id__in=tags)

        preco_min = self.cleaned_data['preco_min']
        if preco_min:
            produtos = produtos.filter(preco__gte=preco_min)

        preco_max = self.cleaned_data['preco_max']
        if preco_max:
            produtos = produtos.filter(preco__lte=preco_max)

        order_by = self.cleaned_data['order_by'] or 'nome'
        order_prefix = '-' if self.cleaned_data['order'] == 'desc' else ''

        produtos = produtos.order_by(f'{order_prefix}{order_by}')

        return produtos.distinct()