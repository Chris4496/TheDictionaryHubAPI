import json
import requests
import collections


def wsearch(word):
    # using thesaurus.com API
    url = f"https://tuna.thesaurus.com/pageData/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    data = requests.get(url, headers=headers)

    json_data = json.loads(data.text)

    if json_data['data'] == None:
        return None
    return json_data


def get_synonyms_and_antonyms(data):
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
    data = wsearch('love')
    if data == None:
        print("No data")
    else:
        print(get_synonyms_and_antonyms(data))
