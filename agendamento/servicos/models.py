from django.db import models

class Usuario(models.Model):
    primeiro_nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    tipo_usuario = models.CharField(max_length=50)

    class Meta:
        db_table = 'usuarios'  # <--- ISSO DIZ AO DJANGO PARA USAR A TABELA QUE JÁ EXISTE