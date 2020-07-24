from lxml import html
import requests, re

# <---------------------| Sites Válidos |-------------------->

def sitesFuncionais(links, sites):
    """
    Passa os links por um processo de filtragem, e retorna apenas os válidos.

    Args:
        links - Lista dos links que serão usados na passagem pelo filtro
        sites - Dicionario que nos values possui os sites usados para a filtragem

    Locals:
        link - Elemento do arg[links] que passara pela aprovação
        site - Value que do arg[sites] que será usado para aprovas os links

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
    """
    Pega o valor dos produtos dos sites da Kabum que forem passados, e os links validos Kabum.

    Args:
        links - Lista de links que serão analisados
        dictSites - Dicionário que, em seus values, contem os sites 'Kabum' validos.

    Locals:
        regex - O 'filtro' dos preços, ira separar os números do resto da string.
        link - Elemento do arg[links] que passara pela aprovação
        page - requests.models.Response | Guarda a resposta do site, (ativo, fora de alcançe, etc.)
        tree - lxml.html.HtmlElement | Possue a informação HTML do site
        precoAdquirido - Lista que ira conter todos os valores adquiridos na página
        preco - arg[precoAdquirido] porém agora editado para uma melhor exibiçao

    Return:
        precoKabum - Lista de todos os preços adquiridos
        sitesKabum - Lista de todos os sites dos quais foram adquiridos os preços
    """

    precoKabum = []
    sitesKabum = []

    regex = re.compile(r"(\d|\d\d|\d\d\d|\d.\d\d\d|\d\d.\d\d\d),\d\d")

    for link in links:
        # Verifica se o link  é da Kabum
        if dictSites['Kabum'] in link:
            page = requests.get(link)
            tree = html.fromstring(page.content)

            precoAdquirido = tree.xpath("//div[@class = 'preco_normal']/text()")

            # Caso o anterior dê errado
            if not precoAdquirido:
                precoAdquirido = tree.xpath("//div[@class = 'preco_antigo-cm']/text()") 

            if precoAdquirido:
                # Formata ele bunitin
                preco = regex.search(precoAdquirido[0]).group()
                preco = float(preco.replace(".", "").replace(",", "."))
                
                # Add o valor e link pra uma lista
                precoKabum.append(f"{preco:.2f}")
                sitesKabum.append(link)

    return precoKabum, sitesKabum

# <---------------------| Mercado Livre |-------------------->

def mercadolivre(links, dictSites):
    """
    Pega o valor dos produtos dos sites do Mercado Livre que forem passados, e os links validos Mercado Livre.

    Args:
        links - Lista de links que serão analisados
        dictSites - Dicionário que, em seus values, contem os sites 'Mercado Livre' validos.

    Locals:

    Return:
        precoML - Lista que contem todos os preços adquiridos
        sitesML - Lista de sites que dos quais foram adquiridos os preços


    """
    precoML = []
    sitesML = []
    listaProdutos = []
    contador = 0
    limitador = numInt("\nSite(s) do Mercado Livre encontrados.\nQuantos produtos dejesa obter? [0 ou para obter todos]\n> ")

    if limitador <= 0:
        limitador = -1

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

                precoML.append(precoFloat + (int(cents[0]) / 100))

                contador += 1

                if contador == limitador:
                    return precoML, sitesML

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
                        sitesML.append(i)

                        precoFloat = int(str(precoAdquirido[0]).replace('.', ''))

                        precoML.append(f"{precoFloat + (int(cents[0]) / 100):.2f}")

                        contador += 1

                        if contador == limitador:
                            return precoML, sitesML     

    return precoML, sitesML

# <---------------------| Número Inteiro |-------------------->

def numInt(msg):
    """
    Exibe uma mensagem e faz o usuário, obrigatoriamente, digitar um número inteiro.

    Args:
        msg - Texto que irá ser exibido

    Attributes:
        limite - Variavel que espera pelo input de um número do usuário

    Return:
        limite - Número inteiro que for digitado
    """
    while True:
        try:
            limite = int(input(msg))
            return limite
        except ValueError:
            print("Tente novamente.")

# <---------------------| Menuzinho |-------------------->

def menu():
    pass