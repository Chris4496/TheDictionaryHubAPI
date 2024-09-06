from bs4 import BeautifulSoup
import requests
from pprint import pprint
import collections


def wsearch(word):
    # using thesaurus.com API
    url = f"https://www.thesaurus.com/browse/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers).text
    doc = BeautifulSoup(page, 'html.parser')

    try:
        entires = doc.find(
            class_="XuslHRKqOSTlhqdz7MbT")
        return entires
    except AttributeError:
        return None


def compileResults(soup):
    meaning_list = list()
    all_defintions_entries = soup.find_all(class_="tU3uvmy24AcyNXg1gHwf")
    for defintion_entry in all_defintions_entries:
        pos_and_def = defintion_entry.find(class_="MzPkuB_wA1zt60pMer_S").find("p")
        [pos, def_] = pos_and_def.text.split("  as in ")

        syn_and_ant = defintion_entry.find_all(class_="flol7HNuPRe9VfZ0KeMZ")
        i = syn_and_ant[0].find_all(class_="fltPJVdHfRCxJJVuGX8J")
        print(len(i))
        # I give up
        # They win
        


def get_synonyms_and_antonyms(entries):
    meaning_list = list()
    all_def = data['data']['definitionData']['definitions']

    for definition in all_def:
        defin = definition['definition']
        pos = definition['pos']
        synonyms = dict()
        antonyms = dict()

        # sort definitions by similarity
        for syn in definition['synonyms']:
            if syn['similarity'] in synonyms:
                synonyms[syn['similarity']].append(syn['term'])
            else:
                synonyms[syn['similarity']] = [syn['term']]

        for ant in definition['antonyms']:
            if ant['similarity'] in antonyms:
                antonyms[ant['similarity']].append(ant['term'])
            else:
                antonyms[ant['similarity']] = [ant['term']]

        meaning_list.append({
            'definition': defin,
            'pos': pos,
            'synonyms': synonyms,
            'antonyms': antonyms
        })

    return meaning_list


if __name__ == "__main__":
    soup = wsearch('cock')
    if soup == None:
        print("No data")
    else:
        print(compileResults(soup))
