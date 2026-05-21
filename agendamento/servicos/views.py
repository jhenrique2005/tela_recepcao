from django.shortcuts import render
from .models import Usuario
import random


def index(request):

    return render(request, 'index.html')


def salvar(request):

    if request.method == 'POST':

        usuario = Usuario.objects.create(

            primeiro_nome=request.POST['primeiro_nome'],
            sobrenome=request.POST['sobrenome'],
            tipo_usuario=request.POST['tipo_usuario'],
            data_nascimento=request.POST['data_nascimento']

        )

        return render(

            request,
            'sucesso.html',

            {
                'numero_sorteio': usuario.id,
                'nome_completo': f"{usuario.primeiro_nome} {usuario.sobrenome}"
            }

        )

    return render(request, 'index.html')


def realizar_sorteio(request):

    usuarios = list(Usuario.objects.all())

    if usuarios:

        ganhador = random.choice(usuarios)

        return render(

            request,
            'sorteio.html',

            {
                'ganhador': ganhador
            }

        )

    return render(

        request,
        'index.html',

        {
            'erro': 'Nenhum participante'
        }

    )

