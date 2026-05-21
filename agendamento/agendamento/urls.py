from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # O admin do Django
    path('admin/', admin.site.urls),
    
    # Isso diz ao Django: "Se a URL não for 'admin', procure as rotas 
    # dentro do arquivo urls.py que está na pasta app_recepcao"
    path('', include('app_recepcao.urls')), 
]