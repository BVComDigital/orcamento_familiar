from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import FieldError, ValidationError
from dateutil import relativedelta
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction

from .forms import LancamentoForm
from .models import CompraParcelada, Lancamento



@login_required
def novo_lancamento(request):

   if request.method == 'POST':
      form = LancamentoForm(request.POST)

      if form.is_valid():

         subcategoria = form.cleaned_data['subcategoria']
         forma_pagamento = form.cleaned_data['forma_pagamento']
         descricao = form.cleaned_data['descricao']
         valor_total = form.cleaned_data['valor_total']
         qtd_parcelas = form.cleaned_data['qtd_parcelas']
         data_vencimento = form.cleaned_data['data_vencimento']
         pago = form.cleaned_data['pago']

         with transaction.atomic():
            compra = None
            if qtd_parcelas > 1:
               compra = CompraParcelada.objects.create(
                  descricao=descricao,
                  valor_total=valor_total,
                  qtd_parcelas=qtd_parcelas,
                  data_compra=data_vencimento
                  )
               

            valor_parcela = (
               valor_total / Decimal(qtd_parcelas)).quantize(Decimal('0.01'),
               rounding=ROUND_HALF_UP
            )

            for numero in range(1, qtd_parcelas + 1):
               data_parcela = data_vencimento + relativedelta(months=numero -1)

               if qtd_parcelas > 1:
                  desc_parcela = f'{descricao} ({numero}/{qtd_parcelas})'
               else:
                  desc_parcela = descricao
               # Marca como pago apenas na 1ª parcela quando o checkbox for marcado
               status_pago = pago if numero == 1 else False
               
               lancamento = Lancamento.objects.create(
                  subcategoria=subcategoria,
                  forma_pagamento=forma_pagamento,
                  compra_parcelada=compra,
                  descricao=descricao, 
                  valor=valor_parcela,
                  data_vencimento=data_parcela,
                  numero_parcela=numero,
                  pago=status_pago,

               )

         if qtd_parcelas > 1:
                messages.success(
                    request,
                    f"Compra parcelada em {qtd_parcelas}x registrada com sucesso!",
                )
         else:
               messages.success(request, "Lançamento registrado com sucesso!")

         return redirect("lista_lancamentos")


            
   else:
      form = LancamentoForm()

   return render(request, 'orcamento/novo_lancamento.html', {'form':form})


@login_required
def lista_lancamentos(request):

   lancamentos = Lancamento.objects.select_related(
       "subcategoria__categoria", "forma_pagamento"
   ).order_by("data_vencimento", "id")

   mes_param = request.GET.get('mes', '').strip()
   ano_param = request.GET.get('ano', '').strip()
   status_param = request.GET.get('status', '').strip()

   if mes_param:
    try:
        mes = int(mes_param)
        if 1 <= mes <= 12:
            lancamentos = lancamentos.filter(data_vencimento__month=mes)
        else:
            messages.warning(request, "Mês inválido. Use um valor entre 1 e 12.")
    except ValueError:
        messages.warning(request, "Mês inválido. Digite um número entre 1 e 12.")

   if ano_param:
    try:
        ano = int(ano_param)
        if ano > 0:
            lancamentos = lancamentos.filter(data_vencimento__year=ano)
        else:
            messages.warning(request, "Ano inválido.")
    except ValueError:
        messages.warning(request, "Ano inválido. Digite um número inteiro.")

   if status_param == "pago":
      lancamentos = lancamentos.filter(pago=True)
   elif status_param == "pendente":
      lancamentos = lancamentos.filter(pago=False)

   contexto = {
       'lancamentos': lancamentos,
       'mes_selecionado': mes_param,
       'ano_selecionado': ano_param,
       'status_selecionado': status_param,
       
   }

   return render(request, 'orcamento/lista_lancamentos.html', contexto)




