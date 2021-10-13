from bs4 import BeautifulSoup
import requests


def wsearch(word):
    word = word.replace(" ", "-")

    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers).text
    doc = BeautifulSoup(page, 'html.parser')

    try:
        entries = doc.find(
            class_="hfl-s lt2b lmt-10 lmb-25 lp-s_r-20 x han tc-bd lmt-20 english").find_all(class_="pr entry-body__el")
        return entries
    except AttributeError:
        return None


def compileResult(entries):
    id = 0
    res = list()
    for entry in entries:
        # get the word
        word = entry.find(class_="hw dhw").text

        # get the word type
        wordType = entry.find(class_="pos dpos").text

        # get the list of audio tags
        audioTags = []
        for tag in entry.find_all(class_="region dreg"):
            audioTags.append(tag.text)

        # get the list of audio links
        audioLinks = []
        for tag in entry.find_all('source', {"type": "audio/mpeg"}):
            audioLinks.append("https://dictionary.cambridge.org" + tag['src'])

        # merge the two lists
        mergedAudioList = []
        for tag, link in zip(audioTags, audioLinks):
            mergedAudioList.append({"tag": tag,
                                    "link": link})

        groups = entry.find_all(class_="def-block ddef_block")
        explanation = list()
        for group in groups:
            groupList = list()
            groupText = group.find_all(
                True, {"class": ["def ddef_d db", "eg deg"]})
            for text in groupText:
                c = ' '.join(text['class'])
                if c == "def ddef_d db":
                    groupList.append(
                        {
                            "type": "main",
                            "content": text.text
                        }
                    )
                elif c == "eg deg":
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
    entries = wsearch("soup")
    res = compileResult(entries)
