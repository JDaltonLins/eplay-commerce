from django import forms

from manager.models.produtos import PedidoDesconto, Produto, CarrinhoItem


class CarrinhoAction(forms.Form):
    id = forms.IntegerField(min_value=1)
    quantidade = forms.IntegerField(min_value=1, required=False)
    force = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        produto_id = cleaned_data.get('id')
        qntd = cleaned_data.get('quantidade') or 1

        if produto_id:
            try:
                produto = Produto.objects.get(id=produto_id, ativo=True)
                cleaned_data['produto'] = produto
                if qntd > produto.estoque:
                    self.add_error(
                        'quantidade', 'Quantidade maior que o estoque')
            except Produto.DoesNotExist:
                self.add_error('id', 'Produto não encontrado')

        return cleaned_data

    def delete(self, user):
        try:
            CarrinhoItem.objects.get(
                user=user, produto=self.cleaned_data['produto']).delete()
            print('deletado')
            return {'status': 'success'}
        except Exception as e:
            return {
                'status': 'error'
            }

    def save(self, user):
        result, created = CarrinhoItem.objects.get_or_create(
            user=user, produto=self.cleaned_data['produto'], defaults={'quantidade': 1})
        if not created:
            if self.cleaned_data['force']:
                result.quantidade += self.cleaned_data['quantidade'] or 1

                if result.quantidade > self.cleaned_data['produto'].estoque:
                    return {
                        'status': 'error',
                        'quantidade': result.quantidade
                    }
            else:
                return {
                    'status': 'error',
                    'quantidade': result.quantidade
                }

        result.save()
        return {'status': 'success', 'quantidade': result.quantidade}


class CarrinhoFinalizar(forms.Form):
    cupom = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        cupom = cleaned_data.get('cupom')
        if cupom:
            try:
                cleaned_data['cupom'] = PedidoDesconto.objects.get(
                    codigo=cupom, retorno='C')
            except PedidoDesconto.DoesNotExist:
                self.add_error('cupom', 'Cupom não encontrado')
        return cleaned_data
