import requests
import cloudscraper
from bs4 import BeautifulSoup


class RequestPage:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/104.0.0.0 Safari/537.36"}

    def connectwithsite(self):
        site = requests.get(self.url, headers=self.headers)

        if int(site.status_code) == 403:
            scraper = cloudscraper.create_scraper(delay=10, browser={
                "custom": "ScraperBot/1.0"})  # Site protegido por CloudFlare precisa utilizar esse scrapper
            site = scraper.get(self.url)

        soap = BeautifulSoup(site.content, 'html.parser')

        return soap
