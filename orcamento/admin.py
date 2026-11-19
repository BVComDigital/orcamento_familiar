from django.contrib import admin
from .models import Categoria, CompraParcelada, FormaPagamento, Lancamento, Subcategoria

admin.site.register(Categoria)
admin.site.register(CompraParcelada)
admin.site.register(FormaPagamento)
admin.site.register(Lancamento)
admin.site.register(Subcategoria)
