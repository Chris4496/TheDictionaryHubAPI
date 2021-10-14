from bs4 import BeautifulSoup
import requests


def wsearch(word):
    word = word.lower()
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
    audioSection = entry.find(class_="webtop").find(class_="phonetics")
    if audioSection != None:
        for tag in audioSection.find_all(class_="icon-audio"):
            if 'American' in tag['title']:
                mergedAudioList.append({"tag": "us",
                                        "link": tag['data-src-mp3']})
            elif 'English' in tag['title']:
                mergedAudioList.append({"tag": "uk",
                                        "link": tag['data-src-mp3']})
    try:
        groups = entry.find(
            'ol', {"class": "senses_multiple"}).findAll(class_="sense")
    except AttributeError:
        groups = entry.find(
            'ol', {"class": "sense_single"}).findAll(class_="sense")

    explanation = list()
    for group in groups:
        groupList = list()
        groupText = group.findAll(True,
                                  {"class": ["sensetop", "labels", "variants", "grammar", "def", "use", "examples"]}, recursive=False)
        for text in groupText:
            c = ' '.join(text['class'])
            if c in ["sensetop", "labels", "variants", "grammar", "def", "use"]:
                if text.text.isspace() == False:
                    groupList.append(
                        {
                            "type": "main",
                            "content": text.text
                        }
                    )
            elif c == "examples":
                groupList.append(
                    {
                        "type": "example",
                        "content": text.text
                    }
                )
        explanation.append(groupList)

    res.append(
        {"id": id,
            "word": word,
            "wordType": wordType,
            "audioLinks": mergedAudioList,
            "explanation": explanation
         }
    )
    id += 1

    return res


if __name__ == "__main__":
    res = wsearch("cock")
    print(compileResult(res))
