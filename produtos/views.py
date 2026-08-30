from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
import requests

from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer


# =========================
# API DE PRODUTOS
# =========================

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


# =========================
# API DE CATEGORIAS
# =========================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# =========================
# PRODUTOS
# =========================

def lista_produtos(request):
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()

    return render(
        request,
        'produtos/lista.html',
        {
            'produtos': produtos,
            'categorias': categorias,
        }
    )


def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    return render(
        request,
        'produtos/detalhe.html',
        {'produto': produto}
    )


def cadastrar_produto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')
        categoria_id = request.POST.get('categoria')
        imagem = request.FILES.get('imagem')
        video = request.FILES.get('video')

        produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade=quantidade,
            categoria_id=categoria_id,
            imagem=imagem,
            video=video,
        )
        produto.save()
        return redirect('lista_produtos')

    return render(
        request,
        'produtos/cadastrar.html',
        {'categorias': categorias}
    )


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.quantidade = request.POST.get('quantidade')
        produto.categoria_id = request.POST.get('categoria')

        imagem = request.FILES.get('imagem')
        if imagem:
            produto.imagem = imagem

        video = request.FILES.get('video')
        if video:
            produto.video = video

        produto.save()
        return redirect('lista_produtos')

    return render(
        request,
        'produtos/editar.html',
        {'produto': produto, 'categorias': categorias}
    )


def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')

    return render(request, 'produtos/excluir.html', {'produto': produto})


# =========================
# CATEGORIAS
# =========================

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produtos/categorias.html', {'categorias': categorias})


def cadastrar_categoria(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        if nome:
            Categoria.objects.create(nome=nome, descricao=descricao)
            return redirect('lista_categorias')

    return render(request, 'produtos/cadastrar_categoria.html')


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        categoria.nome = request.POST.get('nome')
        categoria.descricao = request.POST.get('descricao')
        categoria.save()
        return redirect('lista_categorias')

    return render(request, 'produtos/editar_categoria.html', {'categoria': categoria})


def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')

    return render(request, 'produtos/excluir_categoria.html', {'categoria': categoria})


# ==========================================================
# FUNÇÃO AUXILIAR
# LOCALIZAR CIDADE NA API DO OPEN-METEO
# ==========================================================

def localizar_cidade(cidade):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        'name': cidade,
        'count': 1,
        'language': 'pt',
        'format': 'json',
    }

    resposta = requests.get(geo_url, params=geo_params, timeout=10)
    resposta.raise_for_status()

    dados = resposta.json()
    if not dados.get('results'):
        return None

    return dados['results'][0]


# ==========================================================
# CLIMA ATUAL
# ==========================================================

def clima_atual(request):
    cidade_busca = request.GET.get('cidade', '').strip()

    temperatura = None
    umidade = None
    precipitacao = None
    vento = None
    pais = None
    cidade = cidade_busca
    erro = None

    if cidade_busca:
        try:
            local = localizar_cidade(cidade_busca)

            if not local:
                erro = 'Cidade não encontrada.'
            else:
                latitude = local['latitude']
                longitude = local['longitude']
                cidade = local['name']
                pais = local.get('country', '')

                clima_url = 'https://api.open-meteo.com/v1/forecast'
                clima_params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'current': 'temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m',
                    'timezone': 'auto',
                }

                resposta = requests.get(clima_url, params=clima_params, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()

                atual = dados.get('current', {})
                temperatura = atual.get('temperature_2m')
                umidade = atual.get('relative_humidity_2m')
                precipitacao = atual.get('precipitation')
                vento = atual.get('wind_speed_10m')

        except requests.RequestException:
            erro = 'Não foi possível consultar o serviço de clima.'
        except Exception:
            erro = 'Ocorreu um erro ao consultar o clima.'

    return render(
        request,
        'produtos/clima.html',
        {
            'cidade': cidade,
            'pais': pais,
            'temperatura': temperatura,
            'umidade': umidade,
            'precipitacao': precipitacao,
            'vento': vento,
            'erro': erro,
        }
    )


# ==========================================================
# PREVISÃO DO CLIMA
# ==========================================================

def previsao_clima(request):
    cidade_busca = request.GET.get('cidade', '').strip()

    erro = None
    cidade = cidade_busca
    pais = None
    dias = []

    if not cidade_busca:
        erro = 'Digite o nome de uma cidade.'
    else:
        try:
            local = localizar_cidade(cidade_busca)

            if not local:
                erro = 'Cidade não encontrada.'
            else:
                latitude = local['latitude']
                longitude = local['longitude']
                cidade = local['name']
                pais = local.get('country', '')

                clima_url = 'https://api.open-meteo.com/v1/forecast'
                clima_params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max',
                    'forecast_days': 7,
                    'timezone': 'auto',
                }

                resposta = requests.get(clima_url, params=clima_params, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()

                diaria = dados.get('daily', {})
                datas = diaria.get('time', [])
                temperaturas_maximas = diaria.get('temperature_2m_max', [])
                temperaturas_minimas = diaria.get('temperature_2m_min', [])
                chuvas = diaria.get('precipitation_sum', [])
                ventos = diaria.get('wind_speed_10m_max', [])

                for i in range(len(datas)):
                    dias.append({
                        'data': datas[i],
                        'maxima': temperaturas_maximas[i] if i < len(temperaturas_maximas) else None,
                        'minima': temperaturas_minimas[i] if i < len(temperaturas_minimas) else None,
                        'chuva': chuvas[i] if i < len(chuvas) else None,
                        'vento': ventos[i] if i < len(ventos) else None,
                    })

        except requests.RequestException:
            erro = 'Não foi possível consultar a API de previsão.'
        except Exception:
            erro = 'Ocorreu um erro ao consultar a previsão.'

    return render(
        request,
        'produtos/previsao.html',
        {'cidade': cidade, 'pais': pais, 'dias': dias, 'erro': erro}
    )


# ==========================================================
# CHUVA
# ==========================================================

def chuva_clima(request):
    cidade_busca = request.GET.get('cidade', '').strip()

    erro = None
    cidade = cidade_busca
    pais = None
    chuva = None
    probabilidade = None

    if not cidade_busca:
        erro = 'Digite o nome de uma cidade.'
    else:
        try:
            local = localizar_cidade(cidade_busca)

            if not local:
                erro = 'Cidade não encontrada.'
            else:
                latitude = local['latitude']
                longitude = local['longitude']
                cidade = local['name']
                pais = local.get('country', '')

                clima_url = 'https://api.open-meteo.com/v1/forecast'
                clima_params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'current': 'precipitation',
                    'hourly': 'precipitation_probability',
                    'forecast_days': 1,
                    'timezone': 'auto',
                }

                resposta = requests.get(clima_url, params=clima_params, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()

                atual = dados.get('current', {})
                chuva = atual.get('precipitation')

                probabilidades = dados.get('hourly', {}).get('precipitation_probability', [])
                if probabilidades:
                    probabilidade = max(probabilidades)

        except requests.RequestException:
            erro = 'Não foi possível consultar a API de chuva.'
        except Exception:
            erro = 'Ocorreu um erro ao consultar a chuva.'

    return render(
        request,
        'produtos/chuva.html',
        {'cidade': cidade, 'pais': pais, 'chuva': chuva, 'probabilidade': probabilidade, 'erro': erro}
    )


# ==========================================================
# VENTO
# ==========================================================

def vento_clima(request):
    cidade_busca = request.GET.get('cidade', '').strip()

    erro = None
    cidade = cidade_busca
    pais = None
    vento = None

    if not cidade_busca:
        erro = 'Digite o nome de uma cidade.'
    else:
        try:
            local = localizar_cidade(cidade_busca)

            if not local:
                erro = 'Cidade não encontrada.'
            else:
                latitude = local['latitude']
                longitude = local['longitude']
                cidade = local['name']
                pais = local.get('country', '')

                clima_url = 'https://api.open-meteo.com/v1/forecast'
                clima_params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'current': 'wind_speed_10m,wind_direction_10m,wind_gusts_10m',
                    'timezone': 'auto',
                }

                resposta = requests.get(clima_url, params=clima_params, timeout=10)
                resposta.raise_for_status()
                dados = resposta.json()

                atual = dados.get('current', {})
                vento = {
                    'velocidade': atual.get('wind_speed_10m'),
                    'direcao': atual.get('wind_direction_10m'),
                    'rajada': atual.get('wind_gusts_10m'),
                }

        except requests.RequestException:
            erro = 'Não foi possível consultar a API de vento.'
        except Exception:
            erro = 'Ocorreu um erro ao consultar o vento.'

    return render(
        request,
        'produtos/vento.html',
        {'cidade': cidade, 'pais': pais, 'vento': vento, 'erro': erro}
    )


# ==========================================================
# CADASTRAR VÍDEO
# ==========================================================

def cadastrar_video(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        video = request.FILES.get('video')

        if video:
            produto.video = video
            produto.save()

        return redirect('detalhe_produto', id=produto.id)

    return render(request, 'produtos/imagem', {'produto': produto})

