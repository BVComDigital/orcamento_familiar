from django.db import models

class Categoria(models.Model):
   TIPO_CHOICES = [
      ('R', 'Receita'),
      ('D', 'Despesa')
   ]
   nome = models.CharField(max_length=100, unique=True)
   tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

   def __str__(self):
      return f'{self.nome} ({self.get_tipo_display()})'

class Subcategoria(models.Model):
   categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
   nome = models.CharField(max_length=100)

   def __stf__(self):
      return f'{self.categoria.nome} > {self.nome}'

class FormaPagamento(models.Model):
   nome = models.CharField(max_length=100, unique=True)
   eh_cartao_credito = models.BooleanField(default=False)
   dia_fechamento = models.IntegerField(null=True, blank=True)

   def __str__(self) -> str:
      return self.nome
   
class CompraParcelada(models.Model):
   descricao = models.CharField(max_length=200)
   valor_total = models.DecimalField(max_digits=10, decimal_places=2)
   qtd_parcelas = models.IntegerField()
   data_compra = models.DateField()

   def __str__(self):
      return f"{self.descricao} ({self.qtd_parcelas}x de R$ {self.valor_total / self.qtd_parcelas:.2f})"

class Lancamento(models.Model):
   subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT)
   forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
   compra_parcelada = models.ForeignKey(CompraParcelada, on_delete=models.CASCADE, null=True, blank=True)
   descricao = models.CharField(max_length=200) # Ex: Supermercado semanal, Parcela 1/10
   valor = models.DecimalField(max_digits=10, decimal_places=2)
   data_vencimento = models.DateField() # Define o mês/ano que entra no orçamento
   numero_parcela = models.IntegerField(default=1)
   pago = models.BooleanField(default=False)
   def __str__(self):
      status = "Pago" if self.pago else "Pendente"
      return f'{self.data_vencimento.strftime('%m/%Y')} - {self.descricao}: R$ {self.valor} [{status}]'