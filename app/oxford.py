from bs4 import BeautifulSoup
import requests


def wsearch(word):
    word = word.replace(" ", "-")

    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers).text
    doc = BeautifulSoup(page, 'html.parser')

    try:
        entry = doc.find(
            class_="entry")
        return entry
    except AttributeError:
        return None


def compileResult(entry):
    id = 0
    res = list()

    # get the word
    word = entry.find(class_="headword").text

    # get the word type
    wordType = entry.find(class_="pos").text

    # get the list of audio tags
    mergedAudioList = []
    for tag in entry.find(class_="top-container").find_all(class_="icon-audio"):
        if 'American' in tag['title']:
            mergedAudioList.append({"tag": "us",
                                    "link": tag['data-src-mp3']})
        elif 'English' in tag['title']:
            mergedAudioList.append({"tag": "uk",
                                    "link": tag['data-src-mp3']})

    try:
        groups = entry.find(class_="senses_multiple").find_all("sense")
    except AttributeError:
        print('hi')
        groups = entry.find(class_="sense_single").find_all('sense')

    print(word)
    print(wordType)
    print(mergedAudioList)
    print(groups)


if __name__ == "__main__":
    res = wsearch("cock")
    compileResult(res)
