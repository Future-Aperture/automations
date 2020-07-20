from lxml import html
import requests, re

# <---------------------| Sites Válidos |-------------------->

def sitesFuncionais(links, sites):
    sitesUsados = []

    for j in links:
        for l in sites.values():
            if l in j:
                sitesUsados.append(j)
    
    return sitesUsados

# <---------------------| Kabum |-------------------->

def kabum(links, dictSites):
    # Listas de preço e sites
    mKabum = []
    sKabum = []

    # Para cada link da lista de links
    for i in links:
        # Verifica se o link está certo
        if dictSites['Kabum'] in i:
            # Pega o conteúdo do link
            page = requests.get(i)
            tree = html.fromstring(page.content)
            
            # Filtro dos preços
            regex = re.compile(r"(\d|\d\d|\d\d\d|\d.\d\d\d|\d\d.\d\d\d),\d\d")

            # Preços Adiquiridos
            precoAdquirido = tree.xpath("//div[@class = 'preco_normal']/text()")

            # Caso o anterior dê errado
            if not precoAdquirido:
                precoAdquirido = tree.xpath("//div[@class = 'preco_antigo-cm']/text()") 

            # Caso algum valor seja obtido
            if precoAdquirido:
                # Formata ele bunitin
                preco = regex.search(precoAdquirido[0]).group()
                valor = float(preco.replace(".", "").replace(",", "."))
                
                # Add o valor e link pra uma lista
                mKabum.append(f"{valor:2f}")
                sKabum.append(i)

    # Retorna a lista de preços e sites
    return mKabum, sKabum

# <---------------------| Mercado Livre |-------------------->

def mercadolivre(links, dictSites):
    mML = []
    sML = []
    fodase = []

    for j in links:
        if not links.count(j) > 1:
            if dictSites['Mercado Livre 1'] or dictSites['Mercado Livre 2'] or dictSites['Mercado Livre 3'] or dictSites['Mercado Livre 4'] or dictSites['Mercado Livre 5'] in i:
                # Pega o conteúdo do link
                page = requests.get(j)
                tree = html.fromstring(page.content)

                precoAdquirido = tree.xpath("//span[@class = 'price-tag-fraction']/text()")
                cents = tree.xpath("//span[@class = 'price-tag-cents-visible']/text()")

                if not cents:
                    cents = tree.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

                if precoAdquirido:
                    mML.append(precoAdquirido[0] + (int(cents[0]) / 100))


                if not precoAdquirido:
                    mlSites = tree.xpath("//a[@class = 'item-link item__js-link']")
                    
                    for pinto in mlSites:
                        if pinto not in fodase:
                            fodase.append(pinto.attrib['href'])

                    for i in fodase:
                        page2 = requests.get(i)
                        tree2 = html.fromstring(page2.content)

                        precoAdquirido = tree2.xpath("//span[@class = 'price-tag-fraction']/text()")
                        cents = tree2.xpath("//span[@class = 'price-tag-cents-visible']/text()")

                        if not cents:
                            cents = tree2.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

                        if precoAdquirido:
                            sML.append(i)

                            precoFloat = int(str(precoAdquirido[0]).replace('.', ''))

                            mML.append(f"{precoFloat + (int(cents[0]) / 100):2f}")

    return mML, sML