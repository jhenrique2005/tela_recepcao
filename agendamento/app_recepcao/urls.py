from django.urls import path
from . import views  # Aqui o ponto funciona, pois views.py está nesta pasta

urlpatterns = [
    path('', views.index, name='index'),
    path('salvar/', views.salvar, name='salvar'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('sorteio/', views.pagina_sorteio, name='pagina_sorteio'),
    path('api/sortear', views.api_sortear, name='api_sortear'),
    path('api-impressao/<str:tela>/', views.api_impressao),
]