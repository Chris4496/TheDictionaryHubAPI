from bs4 import BeautifulSoup
import requests


def get_WoTD():
    url = "https://www.merriam-webster.com/word-of-the-day"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')

    word = soup.find(class_="word-and-pronunciation").find('h1').text

    return word.strip()
