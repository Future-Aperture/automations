from lxml import html
from googlesearch import search
import requests, re, functions


# <---------------------||-------------------->

listaPreco = [] # Preços
sites = [] # Sites que serão usados
regex = re.compile(r"(\d|\d\d|\d\d\d|\d.\d\d\d|\d\d.\d\d\d),\d\d") # Filtro dos preços
dictSites = {'Mercado Livre': 'produto.mercadolivre.com.br', 'Kabum': 'kabum.com.br'}

# <---------------------||-------------------->

busca = input("Digite o que você quer buscar:\n> ")

links = search(busca, num = 10, start = 0, stop = 10, pause = 2)

sites = functions.sitesFuncionais(links, dictSites)

# <---------------------||-------------------->

for k in sites.copy():
    page = requests.get(k)
    tree = html.fromstring(page.content)

    precoAdquirido = functions.pegarPreco(sites, dictSites, tree)

    print(precoAdquirido)
    if precoAdquirido:
        preco = regex.search(precoAdquirido).group()
        listaPreco.append(precoAdquirido)

    else:
        sites.remove(k)

# <---------------------||-------------------->

print(listaPreco)
print(f"Sites usados: {sites}")

# <---------------------||-------------------->
# Tudo aqui em baixo é temporario

arquivo = open(".\\listamuitoboa.txt", "w+")

functions.escrever(arquivo, listaPreco, busca, sites, dictSites)

arquivo.close()