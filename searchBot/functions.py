def sitesFuncionais(links, sites):
    sitesUsados = []

    for j in links:
        for l in sites.values():
            if l in j:
                sitesUsados.append(j)
    
    return sitesUsados


def pegarPreco(links, dictSites, tree):
    for i in links:
        if dictSites['Kabum'] in i:
            precoAdquirido = tree.xpath("//div[@class = 'preco_normal']/text()")

            if not precoAdquirido:
                precoAdquirido = tree.xpath("//div[@class = 'preco_antigo-cm']/text()")

            precoAdquirido = ''.join(precoAdquirido)

            return precoAdquirido

        elif dictSites['Mercado Livre 1'] or dictSites['Mercado Livre 2'] in i:
            precoFloat = []

            precoAdquirido = tree.xpath("//span[@class = 'price-tag-fraction']/text()")
            cents = tree.xpath("//span[@class = 'price-tag-cents-visible']/text()")

            if not cents:
                cents = tree.xpath("//span[@class = 'price-tag-cents']/text()") or 0

            cents = ''.join(cents)
            cents = int(cents)

            for i in precoAdquirido:
                precoFloat.append(int(i))

            precoAdquirido = max(precoFloat) + (cents / 100)

            return f"{precoAdquirido:.2f}".replace('.', ',')