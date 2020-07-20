from lxml import html
import requests


k = r'https://www.mercadolivre.com.br/placa-de-video-nvidia-pcyes-geforce-700-series-gtx-750-ti-ppv750ti12802d5-2gb/p/MLB13876104?source=search#searchVariation=MLB13876104&position=1&type=product&tracking_id=fe9e7cfd-af42-4386-8275-9a41928fe015'

newList = [] # LISTA COM OS LINKS

pageF = requests.get(k)
treeF = html.fromstring(pageF.content)

mlSites = treeF.xpath("//a[@class = 'item-link item__js-link']")

for j in mlSites:
    newList.append(j.attrib['href'])

precoFloat = []

for i in newList:
    print(i)
    page = requests.get(i)
    tree = html.fromstring(page.content)

    precoAdquirido = tree.xpath("//span[@class = 'price-tag-fraction']/text()")
    cents = tree.xpath("//span[@class = 'price-tag-cents-visible']/text()")


    if not cents:
        cents = tree.xpath("//span[@class = 'price-tag-cents']/text()") or [0]

    precoFloat = int(str(precoAdquirido[0]).replace('.', ''))

    precoAdquirido = precoFloat + (int(cents[0]) / 100)
    print(precoAdquirido)