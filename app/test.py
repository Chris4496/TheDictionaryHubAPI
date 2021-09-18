import requests

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
headers = {'User-Agent': user_agent}

page = requests.get(
    "https://dictionary.cambridge.org/dictionary/english/cock", headers=headers).text
print(page)
