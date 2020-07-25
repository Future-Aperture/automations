import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.kabum.com.br/hardware/placa-de-video-vga/amd-ati')

soup = BeautifulSoup(page.text, 'html.parser')

titulos = soup.find(class_ = "ec-internal-promotion bg_prime")

print(titulos)