import time
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

first_pokemon_number = 1
last_pokemon_number = 905

pokemon = {}


def getNameAndNumbers(soup):
    pokemon_name_div = soup.find("div", "pokedex-pokemon-pagination-title")
    pokemon_name_div_text = pokemon_name_div.div.text.strip().splitlines()
    pokemon_name = pokemon_name_div_text[0]
    pokemon_number = pokemon_name_div_text[1].strip()
    pokemon["name"] = pokemon_name
    pokemon["number"] = pokemon_number


def getFormes(soup):
    pokemon["forme"] = []
    pokemon_images_div = soup.find("div", "profile-images")
    pokemon_images_div_images = pokemon_images_div.find_all("img")
    # Multiple images based on forme
    for index, pokemon_image in enumerate(pokemon_images_div_images):
        # Forme
        pokemon["forme"].insert(index, {"forme": pokemon_image['alt']})
        # Image
        pokemon["forme"][index].update({"image": pokemon_image['src']})


def getDescriptions(soup):
    pokemon_description_div = soup.find("div", "pokedex-pokemon-details-right")
    pokemon_description_div_version_div = pokemon_description_div.find_all(
        "div", "version-descriptions")
    # Multiple descriptions for different formes
    for index, pokemon_description_forme in enumerate(pokemon_description_div_version_div):
        descriptions = []
        # Different description for each versions
        pokemon_description_x = pokemon_description_forme.find(
            "p", "version-x").get_text().strip()
        pokemon_description_y = pokemon_description_forme.find(
            "p", "version-y").get_text().strip()
        descriptions.append(pokemon_description_x)
        descriptions.append(pokemon_description_y)
        pokemon["forme"][index].update({"descriptions": descriptions})


def getTypes(soup):
    pokemon_type_div = soup.find_all("div", "dtm-type")
    for index, pokemon_type_div_forme in enumerate(pokemon_type_div):
        types = []
        pokemon_type_div_list = pokemon_type_div_forme.find_all("li")
        for pokemon_type in pokemon_type_div_list:
            types.append(pokemon_type.a.get_text())
        pokemon["forme"][index].update({"types": types})


def getWeaknesses(soup):
    pokemon_weaknesses_div = soup.find_all("div", "dtm-weaknesses")
    for index, pokemon_weaknesses_div_forme in enumerate(pokemon_weaknesses_div):
        weaknesses = []
        pokemon_weaknesses_div_list = pokemon_weaknesses_div_forme.find_all(
            "li")
        for pokemon_weakness in pokemon_weaknesses_div_list:
            weaknesses.append(pokemon_weakness.a.span.text.strip())
            pokemon["forme"][index].update({"weaknesses": weaknesses})


def getHeightAndWeight(soup):
    pokemon_body_div = soup.find_all("div", "pokemon-ability-info")
    for index, pokemon_body_div_forme in enumerate(pokemon_body_div):
        pokemon_body_div_list = pokemon_body_div_forme.div.find_all("li")
        # Height
        pokemon["forme"][index].update(
            {"height": pokemon_body_div_list[0].find("span", "attribute-value").get_text()})
        # Weight
        pokemon["forme"][index].update(
            {"weight": pokemon_body_div_list[1].find("span", "attribute-value").get_text()})


def getEvolutions(soup):
    pokemon_evolution_list = soup.find("ul", "evolution-profile")
    pokemon_evolution_first = pokemon_evolution_list.find("li", "first")
    pokemon_evolution_middle = pokemon_evolution_list.find("li", "middle")
    pokemon_evolution_last = pokemon_evolution_list.find("li", "last")
    # First evolution
    first_evolutions = []
    if pokemon_evolution_first is not None:
        first_evolutions.append({"name": pokemon_evolution_first.h3.text.split()[
            0], "image": pokemon_evolution_first.img['src'], "number": pokemon_evolution_first.h3.text.split()[1]})
        pokemon_evolution_first_attributes = pokemon_evolution_first.find_all(
            "li")
        evolution_types = []
        for pokemon_evolution_first_attribute in pokemon_evolution_first_attributes:
            evolution_types.append(pokemon_evolution_first_attribute.text)
        first_evolutions[0].update({"types": evolution_types})
    # Middle evolutions
    middle_evolutions = []
    if pokemon_evolution_middle is not None:
        pokemon_evolution_middle_list_children = pokemon_evolution_middle
        # Evolution images
        pokemon_evolution_middle_list_children_images = pokemon_evolution_middle_list_children.find_all(
            "img")
        for index, pokemon_evolution_middle_list_children_image in enumerate(pokemon_evolution_middle_list_children_images):
            middle_evolutions.append({"image":
                                      pokemon_evolution_middle_list_children_image['src']})
        # Evolution name and number
        pokemon_evolution_middle_list_children_details = pokemon_evolution_middle_list_children.find_all(
            "h3")
        for index, pokemon_evolution_middle_list_children_detail in enumerate(pokemon_evolution_middle_list_children_details):
            middle_evolutions[index].update({"name": pokemon_evolution_middle_list_children_detail.get_text(
            ).rsplit()[0], "number": pokemon_evolution_middle_list_children_detail.get_text().rsplit()[1]})
        # Evolution types
        pokemon_evolution_middle_list_children_attributes_list = pokemon_evolution_middle_list_children.find_all(
            "ul", "evolution-attributes")
        # An evolution
        for index, pokemon_evolution_middle_list_children_attributes in enumerate(pokemon_evolution_middle_list_children_attributes_list):
            pokemon_evolution_middle_list_children_attribute_list = pokemon_evolution_middle_list_children_attributes.find_all(
                "li")
            # Types of particular evolution
            evolution_types = []
            for pokemon_evolution_middle_list_children_type in pokemon_evolution_middle_list_children_attribute_list:
                evolution_types.append(
                    pokemon_evolution_middle_list_children_type.get_text())
            middle_evolutions[index].update({"types": evolution_types})
    # Last evolutions
    last_evolutions = []
    if pokemon_evolution_last is not None:
        pokemon_evolution_last_list_children = pokemon_evolution_last
        # Evolution images
        pokemon_evolution_last_list_children_images = pokemon_evolution_last_list_children.find_all(
            "img")
        for index, pokemon_evolution_last_list_children_image in enumerate(pokemon_evolution_last_list_children_images):
            last_evolutions.append(
                {"image": pokemon_evolution_last_list_children_image['src']})
        # Evolution name and number
        pokemon_evolution_last_list_children_details = pokemon_evolution_last_list_children.find_all(
            "h3")
        for index, pokemon_evolution_last_list_children_detail in enumerate(pokemon_evolution_last_list_children_details):
            last_evolutions[index].update({"name": pokemon_evolution_last_list_children_detail.get_text(
            ).rsplit()[0], "number": pokemon_evolution_last_list_children_detail.get_text().rsplit()[1]})
        # Evolution types
        pokemon_evolution_last_list_children_attributes_list = pokemon_evolution_last_list_children.find_all(
            "ul", "evolution-attributes")
        # An evolution
        for index, pokemon_evolution_last_list_children_attributes in enumerate(pokemon_evolution_last_list_children_attributes_list):
            pokemon_evolution_last_list_children_attribute_list = pokemon_evolution_last_list_children_attributes.find_all(
                "li")
            # Types of particular evolution
            evolution_types = []
            for pokemon_evolution_last_list_children_type in pokemon_evolution_last_list_children_attribute_list:
                evolution_types.append(
                    pokemon_evolution_last_list_children_type.get_text())
            last_evolutions[index].update({"types": evolution_types})
    pokemon["evolution"] = {"first": first_evolutions}
    pokemon["evolution"].update({"middle": middle_evolutions})
    pokemon["evolution"].update({"last": last_evolutions})


def getCards(soup):
    cards = []
    pokemon_cards_list = soup.find(
        "section", id="trading-card-slider").find("ul", "slider").find_all("li")
    for pokemon_card in pokemon_cards_list:
        card_details = pokemon_card.a.find("div", "card-name")
        cards.append({
            "name": card_details.h5.get_text(),
            "number": card_details.find("span", "card-number").get_text(),
            "image": pokemon_card.a.find("div", "card-img").img['data-preload-src'],
            "expansionSymbol": card_details.img['src'],
            "expansionName":  card_details.find("span", "expansion-name").get_text()})
    pokemon["cards"] = cards


for current_pokemon_number in range(first_pokemon_number, last_pokemon_number+1):
    url = f"https://www.pokemon.com/us/pokedex/{current_pokemon_number}"
    req = requests.get(url, headers)

    soup = BeautifulSoup(req.content, 'html.parser')

    # Pokemon name and number
    getNameAndNumbers(soup)

    # Pokemon formes and images
    getFormes(soup)

    # Pokemon description
    getDescriptions(soup)

    # Pokemon type
    getTypes(soup)

    # Pokemon weaknesses
    getWeaknesses(soup)

    # Pokemon height and weight
    getHeightAndWeight(soup)

    # Pokemon evolution
    getEvolutions(soup)

    # Pokemon cards
    getCards(soup)

    print(json.dumps(pokemon, indent=4), ",")
    time.sleep(10)
