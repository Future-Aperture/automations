from lxml import html
import requests, re

def sitesFuncionais(links, sites):
    sitesUsados = []

    for j in links:
        for l in sites.values():
            if l in j:
                sitesUsados.append(j)
    
    return sitesUsados

# <---------------------||-------------------->

def pegarPreco(links, dictSites, tree):
    for i in links:
        if dictSites['Kabum'] in i:
            money = []
            
            regex = re.compile(r"(\d|\d\d|\d\d\d|\d.\d\d\d|\d\d.\d\d\d),\d\d") # Filtro dos preços

            precoAdquirido = tree.xpath("//div[@class = 'preco_normal']/text()")

            if not precoAdquirido:
                precoAdquirido = tree.xpath("//div[@class = 'preco_antigo-cm']/text()")

            precoAdquirido = ''.join(precoAdquirido)

            if precoAdquirido:
                preco = regex.search(precoAdquirido).group()
                money.append(preco)
                newList.append()

            else:
                sites.remove(k)

            return money, newList

    # <---------------------||-------------------->

        elif dictSites['Mercado Livre 1'] or dictSites['Mercado Livre 2'] or dictSites['Mercado Livre 3'] or dictSites['Mercado Livre 4'] in i:
            precoFloat = []
            money = []

            precoAdquirido = tree.xpath("//span[@class = 'price-tag-fraction']/text()")
            cents = tree.xpath("//span[@class = 'price-tag-cents-visible']/text()")

            if not cents:
                cents = tree.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

            if not precoAdquirido:
                newList = [] # LISTA COM OS LINKS

                mlSites = tree.xpath("//a[@class = 'item-link item__js-link']")

                for j in mlSites:
                    newList.append(j.attrib['href'])
                
                for i in newList:
                    page2 = requests.get(i)
                    tree2 = html.fromstring(page2.content)

                    precoAdquirido = tree2.xpath("//span[@class = 'price-tag-fraction']/text()")
                    cents = tree2.xpath("//span[@class = 'price-tag-cents-visible']/text()")

                    if not cents:
                        cents = tree2.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

                    precoFloat = int(str(precoAdquirido[0]).replace('.', ''))

                    money.append(f"{precoFloat + (int(cents[0]) / 100):.2f}".replace('.', ','))

                return money, newList

            for i in precoAdquirido:
                precoFloat.append(int(i) + 1)

            money.append(precoFloat + (int(cents[0]) / 100))

            return money, newList
        
    # <---------------------||-------------------->

def pegarKabum(links, dictSites, tree):
    pass

def pegarML(links, dictSites, tree):
    pass