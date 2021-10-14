from bs4 import BeautifulSoup
import requests


def wsearch(word):
    word = word.replace(" ", "%20")

    url = f"https://www.merriam-webster.com/dictionary/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers).text
    doc = BeautifulSoup(page, 'html.parser')

    try:
        entries = doc.find(
            class_="left-content col-lg-7 col-xl-8")

        # get rid of more defs
        for div in entries.find_all("div", {'class': 'more_defs'}):
            div.decompose()

        return entries
    except AttributeError:
        return None

# TODO add header for section


def compileResult(entries):
    id = 0
    res = list()
    wordList = entries.find_all(class_="hword")

    wordTypeList = list()
    for header in entries.find_all(class_="row entry-header"):
        wordTypeList.append(header.find(class_="important-blue-link"))

    mergedAudioList = list()
    audioSection = entries.find(class_="prs")

    print(wordList)
    print(wordTypeList)


if __name__ == "__main__":
    entries = wsearch("ta")
    res = compileResult(entries)
