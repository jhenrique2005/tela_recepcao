from django.shortcuts import render
from django.http import JsonResponse
from .models import Pessoa
import random
import win32print


fila_impressao = {
    "tela1": [],
    "tela2": [],
}


def imprimir_raw(nome_impressora, texto):

    dados = texto.encode("latin-1")

    hPrinter = win32print.OpenPrinter(nome_impressora)

    try:
        hJob = win32print.StartDocPrinter(
            hPrinter,
            1,
            ("Ticket Sorteio", None, "RAW")
        )

        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, dados)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)

    finally:
        win32print.ClosePrinter(hPrinter)


def index(request):
    return render(request, 'index.html')


def pagina_sorteio(request):
    return render(request, 'sorteio.html')


def salvar(request):

    if request.method == 'POST':

        usuario = Pessoa.objects.create(
            primeiro_nome=request.POST.get('primeiro_nome'),
            sobrenome=request.POST.get('sobrenome'),
            tipo_usuario=request.POST.get('tipo_usuario'),
            data_nascimento=request.POST.get('data_nascimento')
        )

        tela = request.POST.get("tela", "").strip()

        print("TELA RECEBIDA:", tela)

        # --- CONSTANTES ESC/POS ---
        ESC_RESET = "\x1B\x40"
        ESC_ALIGN_CENTER = "\x1B\x61\x01"
        FONT_NORMAL = "\x1B\x21\x00"
        FONT_DOUBLE_HEIGHT = "\x1B\x21\x10"
        FONT_DOUBLE_WIDTH = "\x1B\x21\x20"
        FONT_BIG = "\x1D\x21\x11"
        FONT_MEDIUM = "\x1D\x21\x01"
        PAPER_CUT = "\x1D\x56\x00"

# --- MONTAGEM DO CONTEÚDO ---
# Atenção: O texto dentro das aspas deve ficar encostado na margem esquerda
# para evitar que a impressora receba espaços indesejados ou dê erro no Python.
        conteudo = f"""{ESC_RESET}{ESC_ALIGN_CENTER}{FONT_DOUBLE_HEIGHT}CADASTRO REALIZADO\n
{FONT_NORMAL}====================
{FONT_DOUBLE_HEIGHT}GUARDE SEU NUMERO\n
{FONT_BIG}{usuario.id}
{FONT_NORMAL}====================\n
{FONT_DOUBLE_WIDTH}BOA SORTE!
{FONT_NORMAL}{FONT_MEDIUM}{usuario.primeiro_nome} {usuario.sobrenome}
{FONT_NORMAL}\n\n\n\n
{PAPER_CUT}"""
        if tela in fila_impressao:

            fila_impressao[tela].append(conteudo)

            print("COLOQUEI NA FILA:", tela)
            print("FILA TELA1:", len(fila_impressao["tela1"]))
            print("FILA TELA2:", len(fila_impressao["tela2"]))

        else:

            print("SEM TELA / CELULAR - IMPRIMINDO NO SERVIDOR")

            try:
                impressora = "Sorteio"

                imprimir_raw(impressora, conteudo)

                print("IMPRESSÃO SERVIDOR ENVIADA!")

            except Exception as e:
                print(f"Erro impressão servidor: {e}")

        return render(request, 'sucesso.html', {
            'numero_sorteio': usuario.id,
            'nome_completo': f"{usuario.primeiro_nome} {usuario.sobrenome}",
            'tela': tela
        })

    return render(request, 'index.html')


def api_impressao(request, tela):

    print("API CONSULTADA:", tela)

    if tela in fila_impressao and fila_impressao[tela]:

        texto = fila_impressao[tela].pop(0)

        print("ENVIANDO IMPRESSÃO PARA:", tela)

        return JsonResponse({
            "imprimir": True,
            "texto": texto
        })

    return JsonResponse({
        "imprimir": False
    })


def realizar_sorteio(request):

    usuarios = list(Pessoa.objects.all())

    if usuarios:
        ganhador = random.choice(usuarios)
        return render(request, 'sorteio.html', {'ganhador': ganhador})

    return render(request, 'index.html', {'erro': 'Nenhum participante'})


def api_sortear(request):

    usuarios = list(Pessoa.objects.all())

    if usuarios:
        ganhador = random.choice(usuarios)

        return JsonResponse({
            'id': ganhador.id,
            'primeiro_nome': ganhador.primeiro_nome,
            'sobrenome': ganhador.sobrenome
        })

    return JsonResponse({'erro': 'Nenhum participante'})


def sucesso(request):
    return render(request, 'sucesso.html', {'numero_sorteio': '---'})