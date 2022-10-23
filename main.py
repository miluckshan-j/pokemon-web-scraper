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

# Pokemon formes and images
pokemon_images_div = soup.find("div", "profile-images")
pokemon_images_div_images = pokemon_images_div.find_all("img")
# Multiple images based on forme
for pokemon_image in pokemon_images_div_images:
    print()
    # Forme
    # print(pokemon_image['alt'])
    # Image
    # print(pokemon_image['src'])

# Pokemon description
pokemon_description_div = soup.find("div", "pokedex-pokemon-details-right")
pokemon_description_div_version_div = pokemon_description_div.find_all(
    "div", "version-descriptions")
# Multiple descriptions for different formes
for pokemon_description_forme in pokemon_description_div_version_div:
    # Different description for each versions
    pokemon_description_x = pokemon_description_forme.find(
        "p", "version-x").get_text().strip()
    pokemon_description_y = pokemon_description_forme.find(
        "p", "version-y").get_text().strip()
    # print(pokemon_description_x)
    # print(pokemon_description_y)
