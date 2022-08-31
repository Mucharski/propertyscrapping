import requests
from bs4 import BeautifulSoup


class RequestPage:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/104.0.0.0 Safari/537.36"}

    def connectwithsite(self):
        site = requests.get(self.url, headers=self.headers)
        soap = BeautifulSoup(site.content, 'html.parser')

        return soap
