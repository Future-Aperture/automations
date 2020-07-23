from lxml import html
from googlesearch import search
import requests, re, functions

# <---------------------| Variaveis Globais |-------------------->

# Exibição dos sites no txt
sites = ["Mercado Livre", "Kabum"]

# Dict para ser usado nas buscas
dictSites = {   'Mercado Livre 1': 'produto.mercadolivre.com.br',
                'Mercado Livre 2': 'www.mercadolivre.com.br',
                'Mercado Livre 3': 'lista.mercadolivre.com.br',
                'Mercado Livre 4': 'informatica.mercadolivre.com.br',
                'Mercado Livre 5': 'loja.mercadolivre.com.br',
                'Kabum': 'www.kabum.com.br'}

# <---------------------| Sites Usados |-------------------->

# O que vai buscar no google
busca = input("Digite o que você quer buscar:\n> ")

# Quantos links do google ele vai buscar    
limite = functions.numInt()
    
# Pega os links da busca
links = search(query = busca, start = 0, stop = limite, pause = 2)

# Filtra os sites de acordo com o <dictSites>
sites = functions.sitesFuncionais(links, dictSites)

# <---------------------| Busca nos Sites |-------------------->

# Pega os preços e links dos produtos
pKabum, lKabum = functions.kabum(sites, dictSites)
pML, lML = functions.mercadolivre(sites, dictSites)

# Junta todos os preços e links
todosPreco = (pKabum, pML)
todosLinks = (lKabum, lML)

# <---------------------| Debug |-------------------->

# print(pML)
# print(lML)
print("DEU CERTO!!!!!!!!!!!!!!!")

# <---------------------| Arquivo de Texto |-------------------->

arquivo = open(".\\listamuitoboa.txt", "w+")

arquivo.write(f"Busca realizada: {busca}\n\n")

for p in range(len(todosPreco)):
    for i in range(len(todosPreco[p])):
        arquivo.write(f"""Site: Mercado Livre
Preço: R$ {str(todosPreco[p][i]).replace(".", ",")}
Link: {todosLinks[p][i]}

""")

arquivo.close()

