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
                'Mercado Livre 5': 'loja.mercadolivre.com.br',
                'Kabum': 'www.kabum.com.br'}

# <---------------------||-------------------->

busca = input("Digite o que você quer buscar:\n> ")

links = search(busca, num = 10, start = 0, stop = 10, pause = 2)

sites = functions.sitesFuncionais(links, dictSites)

# <---------------------||-------------------->

pKabum, lKabum = functions.kabum(sites, dictSites)
pML, lML = functions.mercadolivre(sites, dictSites)


todosPreco = (pKabum, pML)
todosLinks = (lKabum, lML)
# <---------------------| Debug |-------------------->

# print(pML)
# print(lML)
print("DEU CERTO!!!!!!!!!!!!!!!")

# <---------------------||-------------------->
# Tudo aqui em baixo é temporario

arquivo = open(".\\listamuitoboa.txt", "w+")

arquivo.write(f"Busca realizada: {busca}\n\n")

for p in range(len(todosPreco)):
    for i in range(len(todosPreco[p])):
        arquivo.write(f"""Site: Mercado Livre
Preço: R$ {todosPreco[p][i]}
Link: {todosLinks[p][i]}

""")

arquivo.close()

