import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
url = "https://www.pokemon.com/us/pokedex/1"
req = requests.get(url, headers)

soup = BeautifulSoup(req.content, 'html.parser')

# Pokemon name and number
pokemon_name_div = soup.find("div", "pokedex-pokemon-pagination-title")
pokemon_name_div_text = pokemon_name_div.div.text.strip().splitlines()
pokemon_name = pokemon_name_div_text[0]
pokemon_number = pokemon_name_div_text[1].strip()
# print(pokemon_name)
# print(pokemon_number)
# // Pokemon Name and Number
