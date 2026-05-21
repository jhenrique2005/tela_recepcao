from django.db import models

class Pessoa(models.Model):
    # Esses nomes devem ser os nomes das colunas no seu MySQL
    primeiro_nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    tipo_usuario = models.CharField(max_length=50)

    class Meta:
        db_table = 'usuarios'  # <--- ISSO É O MAIS IMPORTANTE!