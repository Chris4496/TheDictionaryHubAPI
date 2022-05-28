from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse, parse_qs


def wsearch(word):
    # word = word.replace(" ", "%20")

    url = f"https://www.merriam-webster.com/dictionary/{word}"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers).text
    doc = BeautifulSoup(page, 'html.parser')
    try:
        doc.find(class_="more_defs").decompose()
    except AttributeError:
        pass
    try:
        entries = doc.find(id="left-content")
        if entries.find(class_="missing-query") == None and not entries.find(class_="spelling-suggestion-text"):
            return entries

        return None
    except AttributeError:
        print("No results found")
        return None


def compileResult(soup):
    all_entry_headers = soup.find_all(class_="entry-header")
    all_audio = soup.find_all(class_="entry-attr")
    all_entries = soup.find_all(
        'div', {'id': [re.compile(r'dictionary-entry-\d'), re.compile(r'medical-entry-\d')]})

    word_list = list()
    word_type_list = list()
    for header in all_entry_headers:
        word_list.append(header.find(class_='hword').text)
        # if word have no type, it will be None
        try:
            word_type_list.append(header.find('a').text)
        except AttributeError:
            word_type_list.append("")

    merriam_media_base_url = "https://media.merriam-webster.com/audio/prons/en/us/mp3/"
    audio_list = list()
    for audio in all_audio:
        urls = audio.find_all('a')

        temp = list()
        for url in urls:
            try:
                temp.append(url['data-url'])
            except KeyError:
                pass

        urls = temp
        l = list()
        for url in urls:
            query_info = parse_qs(urlparse(url).query)
            l.append(merriam_media_base_url +
                     query_info['dir'][0] + "/" + query_info['file'][0] + ".mp3")
        audio_list.append(l)

    explanation_list = list()
    for entry in all_entries:
        parts = entry.find_all(class_="sb")
        group_list = list()
        for part in parts:
            texts = part.find_all('span', {'class': ['dtText', 'sents']})
            part_list = list()
            for text in texts:
                if 'dtText' in text['class']:
                    # remove the ": " in the beginning of the text
                    part_list.append(
                        {
                            'type': 'main',
                            'content': text.text[2:]

                        }
                    )
                elif 'sents' in text['class']:
                    part_list.append(
                        {
                            'type': 'example',
                            'content': text.text

                        }
                    )
            group_list.append(part_list)
        explanation_list.append(group_list)

    if not audio_list:
        audio_list = [''] * len(word_list)
    elif len(audio_list) < len(word_list):
        # add None if audio_list is shorter than word_list
        audio_list.extend([audio_list[0]] * (len(word_list) - len(audio_list)))

    id = 0
    res = list()
    for word, word_type, audio, explanation in zip(word_list, word_type_list, audio_list, explanation_list):
        audio1 = list()
        for a in audio:
            audio1.append({'tag': 'us', 'link': a})
        res.append(
            {
                'id': id,
                'word': word,
                'wordType': word_type,
                'audioLinks': audio1,
                'explanation': explanation
            }
        )
        id += 1
    return res


if __name__ == "__main__":
    soup = wsearch("pneumonoultramicroscopicsilicovolcanoconiosis")
    if soup is None:
        print("No results found")
    result = compileResult(soup)
    print(result)
