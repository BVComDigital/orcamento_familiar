from decimal import Decimal
from django import forms 
from .models import FormaPagamento, Subcategoria

class LancamentoForm(forms.Form):
   subcategoria = forms.ModelChoiceField(
      queryset=Subcategoria.objects.select_related('categoria').order_by('categoria__nome', 'nome'), label='Subcategoria'
      )

   forma_pagamento = forms.ModelChoiceField(
      queryset=FormaPagamento.objects.order_by('nome'), label='Formad de pagamento'
      )

   descricao = forms.CharField(
      max_length=200, label='Descrição'
   )

   valor_total = forms.DecimalField(
      max_digits=10,
      decimal_places=2,
      min_value=Decimal('0.01'),
      label='Valor total (R$)',
   )

   data_vencimento = forms.DateField(
      label='Data de vencimento (1º parcela)',
      widget=forms.DateInput(attrs={'type': 'date'})
   )

   qtd_parcelas = forms.IntegerField(
      min_value=1,
      initial=1,
      label="Quantidade de parcelas",
   )
   pago = forms.BooleanField(
      required=False,
      initial=False,
      label="Pago",
   )

   


