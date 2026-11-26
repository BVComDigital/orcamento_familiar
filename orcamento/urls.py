from django.urls import path
from . import views

urlpatterns = [
   path('lancamentos/novo', views.novo_lancamento, name='novo_lancamento' ),
   path('lancamentos/', views.lista_lancamentos, name='lista_lancamentos' ),

]
