from lxml import html
import requests, re

# <---------------------| Sites Válidos |-------------------->

def sitesFuncionais(links, sites):
    """
    Passa os links por um processo de filtragem, e retorna apenas os válidos.

    Args:
        link - Lista dos links que serão usados na passagem pelo filtro
        sites - Dicionario que nos values possui os sites usados para a filtragem

    Attributes:
        sitesUsados - Lista que irá armazenar os sites válidos

    Return:
        sitesUsados - Lista de todos os sites que passaram pelo filtro
    """

    sitesUsados = []

    for link in links:
        for site in sites.values():
            if site in link:
                sitesUsados.append(link)
    
    return sitesUsados

# <---------------------| Kabum |-------------------->

def kabum(links, dictSites):
    # Listas de preço e sites
    mKabum = []
    sKabum = []

    # Filtro dos preços
    regex = re.compile(r"(\d|\d\d|\d\d\d|\d.\d\d\d|\d\d.\d\d\d),\d\d")

    # Para cada link da lista de links
    for i in links:
        # Verifica se o link está certo
        if dictSites['Kabum'] in i:
            # Pega o conteúdo do link
            page = requests.get(i)
            tree = html.fromstring(page.content)

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
                mKabum.append(f"{valor:.2f}")
                sKabum.append(i)

    # Retorna a lista de preços e sites
    return mKabum, sKabum

# <---------------------| Mercado Livre |-------------------->

def mercadolivre(links, dictSites):
    mML = []
    sML = []
    listaProdutos = []
    count = 0
    limitador = numInt()

    for j in links:
        if dictSites['Mercado Livre 1'] or dictSites['Mercado Livre 2'] or dictSites['Mercado Livre 3'] or dictSites['Mercado Livre 4'] or dictSites['Mercado Livre 5'] in j:
            # Pega o conteúdo do link
            page = requests.get(j)
            tree = html.fromstring(page.content)

            precoAdquirido = tree.xpath("//span[@class = 'price-tag-fraction']/text()")
            cents = tree.xpath("//span[@class = 'price-tag-cents-visible']/text()")

            if not cents:
                cents = tree.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

            if precoAdquirido:
                precoFloat = int(str(precoAdquirido[0]).replace('.', ''))

                mML.append(precoFloat + (int(cents[0]) / 100))

                count += 1

                if count == limitador:
                    return mML, sML

            else:
                mlSites = tree.xpath("//a[@class = 'item-link item__js-link']")
                
                for hrefLinks in mlSites:
                    if hrefLinks not in listaProdutos:
                        listaProdutos.append(hrefLinks.attrib['href'])

                for i in listaProdutos:
                    page2 = requests.get(i)
                    tree2 = html.fromstring(page2.content)

                    precoAdquirido = tree2.xpath("//span[@class = 'price-tag-fraction']/text()")
                    cents = tree2.xpath("//span[@class = 'price-tag-cents-visible']/text()")

                    if not cents:
                        cents = tree2.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

                    if precoAdquirido:
                        sML.append(i)

                        precoFloat = int(str(precoAdquirido[0]).replace('.', ''))

                        mML.append(f"{precoFloat + (int(cents[0]) / 100):.2f}")

                        count += 1

                        if count == limitador:
                            return mML, sML     

    return mML, sML

# <---------------------| numInteiro |-------------------->

def numInt():
    while True:
        try:
            limite = int(input("\nQuantos links você deseja adquirir?\n> "))
            return limite
        except ValueError:
            print("Tente novamente.")