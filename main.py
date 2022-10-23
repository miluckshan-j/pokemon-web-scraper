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

# Pokemon type
pokemon_type_div = soup.find("div", "dtm-type")
pokemon_type_div_list = pokemon_type_div.find_all("li")
for pokemon_type in pokemon_type_div_list:
    print()
    # print(pokemon_type.a.get_text())

# Pokemon weaknesses
pokemon_weaknesses_div = soup.find("div", "dtm-weaknesses")
pokemon_weaknesses_div_list = pokemon_weaknesses_div.find_all("li")
for pokemon_weakness in pokemon_weaknesses_div_list:
    print()
    # print(pokemon_weakness.a.span.text.rsplit()[0])

# Pokemon height and weight
pokemon_body_div = soup.find("div", "pokemon-ability-info")
pokemon_body_div_list = pokemon_body_div.div.find_all("li")
# Height
# print(pokemon_body_div_list[0].find("span", "attribute-value").get_text())
# Weight
# print(pokemon_body_div_list[1].find("span", "attribute-value").get_text())

# Pokemon evolution
pokemon_evolution_list = soup.find("ul", "evolution-profile")
# print(pokemon_evolution_list.prettify())
pokemon_evolution_first = pokemon_evolution_list.find("li", "first")
pokemon_evolution_middle = pokemon_evolution_list.find("li", "middle")
pokemon_evolution_last = pokemon_evolution_list.find("li", "last")
print("*****************************************************************************")
if pokemon_evolution_first is not None:
    print(pokemon_evolution_first.img['src'])
    print(pokemon_evolution_first.h3.text.split()[0])
    print(pokemon_evolution_first.h3.text.split()[1])
    pokemon_evolution_first_attributes = pokemon_evolution_first.find_all("li")
    for pokemon_evolution_first_attribute in pokemon_evolution_first_attributes:
        print(pokemon_evolution_first_attribute.text)   
print("*****************************************************************************")
# if pokemon_evolution_middle is not None:
#     print(pokemon_evolution_middle.prettify())
# print("*****************************************************************************")
# if pokemon_evolution_last is not None:
#     print(pokemon_evolution_last.prettify())
# print("*****************************************************************************")
