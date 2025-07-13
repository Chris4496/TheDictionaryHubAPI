import requests
from pprint import pprint


def get_synonyms_and_antonyms(word: str):
    synonyms_url = f"https://api.datamuse.com/words?rel_syn={word}"
    antonyms_url = f"https://api.datamuse.com/words?rel_ant={word}"

    try:
        synonyms_response = requests.get(synonyms_url)
        antonyms_response = requests.get(antonyms_url)
        
        synonyms = synonyms_response.json()
        antonyms = antonyms_response.json()
        
        return {
            "synonyms": [item['word'] for item in synonyms],
            "antonyms": [item['word'] for item in antonyms]
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    word = "contrite"
    result = get_synonyms_and_antonyms(word)
    pprint(result)