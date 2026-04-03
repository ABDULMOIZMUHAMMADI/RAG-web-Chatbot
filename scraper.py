import requests
from bs4 import BeautifulSoup


def scrape_website(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    return text