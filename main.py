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
    name_div = soup.find("div", "pokedex-pokemon-pagination-title")
    name_div_text = name_div.div.text.strip().splitlines()
    name = name_div_text[0]
    number = name_div_text[1].strip()
    pokemon["name"] = name
    pokemon["number"] = number


def getFormes(soup):
    pokemon["forme"] = []
    images_div = soup.find("div", "profile-images")
    images_div_images = images_div.find_all("img")
    # Multiple images based on forme
    for index, image in enumerate(images_div_images):
        # Forme
        pokemon["forme"].insert(index, {"forme": image['alt']})
        # Image
        pokemon["forme"][index].update({"image": image['src']})


def getDescriptions(soup):
    description_div = soup.find("div", "pokedex-pokemon-details-right")
    description_div_version_div = description_div.find_all(
        "div", "version-descriptions")
    # Multiple descriptions for different formes
    for index, description_forme in enumerate(description_div_version_div):
        descriptions = []
        # Different description for each versions
        description_x = description_forme.find(
            "p", "version-x").get_text().strip()
        description_y = description_forme.find(
            "p", "version-y").get_text().strip()
        descriptions.append(description_x)
        descriptions.append(description_y)
        pokemon["forme"][index].update({"descriptions": descriptions})


def getTypes(soup):
    type_div = soup.find_all("div", "dtm-type")
    for index, type_div_forme in enumerate(type_div):
        types = []
        type_div_list = type_div_forme.find_all("li")
        for type in type_div_list:
            types.append(type.a.get_text())
        pokemon["forme"][index].update({"types": types})


def getWeaknesses(soup):
    weaknesses_div = soup.find_all("div", "dtm-weaknesses")
    for index, weaknesses_div_forme in enumerate(weaknesses_div):
        weaknesses = []
        weaknesses_div_list = weaknesses_div_forme.find_all(
            "li")
        for weakness in weaknesses_div_list:
            weaknesses.append(weakness.a.span.text.strip())
            pokemon["forme"][index].update({"weaknesses": weaknesses})


def getHeightAndWeight(soup):
    body_div = soup.find_all("div", "pokemon-ability-info")
    for index, body_div_forme in enumerate(body_div):
        body_div_list = body_div_forme.div.find_all("li")
        # Height
        pokemon["forme"][index].update(
            {"height": body_div_list[0].find("span", "attribute-value").get_text()})
        # Weight
        pokemon["forme"][index].update(
            {"weight": body_div_list[1].find("span", "attribute-value").get_text()})


def getEvolutions(soup):
    evolution_list = soup.find("ul", "evolution-profile")
    evolution_first = evolution_list.find("li", "first")
    evolution_middle = evolution_list.find("li", "middle")
    evolution_last = evolution_list.find("li", "last")
    # First evolution
    first_evolutions = []
    if evolution_first is not None:
        first_evolutions.append({"name": evolution_first.h3.text.split()[
            0], "image": evolution_first.img['src'], "number": evolution_first.h3.text.split()[1]})
        evolution_first_attributes = evolution_first.find_all(
            "li")
        evolution_types = []
        for evolution_first_attribute in evolution_first_attributes:
            evolution_types.append(evolution_first_attribute.text)
        first_evolutions[0].update({"types": evolution_types})
    # Middle evolutions
    middle_evolutions = []
    if evolution_middle is not None:
        evolution_middle_list_children = evolution_middle
        # Evolution images
        evolution_middle_list_children_images = evolution_middle_list_children.find_all(
            "img")
        for index, evolution_middle_list_children_image in enumerate(evolution_middle_list_children_images):
            middle_evolutions.append({"image":
                                      evolution_middle_list_children_image['src']})
        # Evolution name and number
        evolution_middle_list_children_details = evolution_middle_list_children.find_all(
            "h3")
        for index, evolution_middle_list_children_detail in enumerate(evolution_middle_list_children_details):
            middle_evolutions[index].update({"name": evolution_middle_list_children_detail.get_text(
            ).rsplit()[0], "number": evolution_middle_list_children_detail.get_text().rsplit()[1]})
        # Evolution types
        evolution_middle_list_children_attributes_list = evolution_middle_list_children.find_all(
            "ul", "evolution-attributes")
        # An evolution
        for index, evolution_middle_list_children_attributes in enumerate(evolution_middle_list_children_attributes_list):
            evolution_middle_list_children_attribute_list = evolution_middle_list_children_attributes.find_all(
                "li")
            # Types of particular evolution
            evolution_types = []
            for evolution_middle_list_children_type in evolution_middle_list_children_attribute_list:
                evolution_types.append(
                    evolution_middle_list_children_type.get_text())
            middle_evolutions[index].update({"types": evolution_types})
    # Last evolutions
    last_evolutions = []
    if evolution_last is not None:
        evolution_last_list_children = evolution_last
        # Evolution images
        evolution_last_list_children_images = evolution_last_list_children.find_all(
            "img")
        for index, evolution_last_list_children_image in enumerate(evolution_last_list_children_images):
            last_evolutions.append(
                {"image": evolution_last_list_children_image['src']})
        # Evolution name and number
        evolution_last_list_children_details = evolution_last_list_children.find_all(
            "h3")
        for index, evolution_last_list_children_detail in enumerate(evolution_last_list_children_details):
            last_evolutions[index].update({"name": evolution_last_list_children_detail.get_text(
            ).rsplit()[0], "number": evolution_last_list_children_detail.get_text().rsplit()[1]})
        # Evolution types
        evolution_last_list_children_attributes_list = evolution_last_list_children.find_all(
            "ul", "evolution-attributes")
        # An evolution
        for index, evolution_last_list_children_attributes in enumerate(evolution_last_list_children_attributes_list):
            evolution_last_list_children_attribute_list = evolution_last_list_children_attributes.find_all(
                "li")
            # Types of particular evolution
            evolution_types = []
            for evolution_last_list_children_type in evolution_last_list_children_attribute_list:
                evolution_types.append(
                    evolution_last_list_children_type.get_text())
            last_evolutions[index].update({"types": evolution_types})
    pokemon["evolution"] = {"first": first_evolutions}
    pokemon["evolution"].update({"middle": middle_evolutions})
    pokemon["evolution"].update({"last": last_evolutions})


def getCards(soup):
    cards = []
    cards_list = soup.find(
        "section", id="trading-card-slider").find("ul", "slider").find_all("li")
    for card in cards_list:
        card_details = card.a.find("div", "card-name")
        cards.append({
            "name": card_details.h5.get_text(),
            "number": card_details.find("span", "card-number").get_text(),
            "image": card.a.find("div", "card-img").img['data-preload-src'],
            "expansionSymbol": card_details.img['src'],
            "expansionName":  card_details.find("span", "expansion-name").get_text()})
    pokemon["cards"] = cards


for current_number in range(first_pokemon_number, last_pokemon_number+1):
    url = f"https://www.pokemon.com/us/pokedex/{current_number}"
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
