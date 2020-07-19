from lxml import html
from googlesearch import search
import requests, re, functions

# <---------------------||-------------------->

listaPreco = [] # Preços
sites = [] # Sites que serão usados
dictSites = {   'Mercado Livre 1': 'produto.mercadolivre.com.br',
                'Mercado Livre 2': 'www.mercadolivre.com.br',
                'Mercado Livre 3': 'lista.mercadolivre.com.br',
                'Mercado Livre 4': 'informatica.mercadolivre.com.br',
                'Kabum': 'kabum.com.br'}

# <---------------------||-------------------->

busca = input("Digite o que você quer buscar:\n> ")

links = search(busca, num = 10, start = 0, stop = 10, pause = 2)

sites = functions.sitesFuncionais(links, dictSites)

# <---------------------||-------------------->

for k in sites.copy():
    page = requests.get(k)
    tree = html.fromstring(page.content)

    precos, linques = functions.pegarPreco(sites, dictSites, tree)

    print(precoAdquirido)



# <---------------------||-------------------->

print(listaPreco)
print(f"Sites usados: {sites}")

# <---------------------||-------------------->
# Tudo aqui em baixo é temporario

arquivo = open(".\\listamuitoboa.txt", "w+")

arquivo.write(f"Busca realizada: {busca}\n\n")

for i in range(len(listaPreco)):
    for k, v in dictSites.items():
        if v in sites[i]:
            arquivo.write(f"""Site: {k}
Preço: R$ {listaPreco[i]}
Link: {sites[i]}

""")

arquivo.close()