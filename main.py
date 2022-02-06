import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import nltk
import json
nltk.download('stopwords')
nltk.download('punkt')

from rake_nltk import Rake
rake_nltk_var = Rake()
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
              path = urljoin(url, path)
            yield path
    def find_meta(self, url, html):
     soup = BeautifulSoup(html, 'html.parser')
     for link in soup.find_all('meta'):
      t = link.get('name')
      if t and t == "description":
       path = link.get("content").replace('.','').replace("\'", '').replace("\"", '')
       return path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        url2 = url
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
        	self.add_url_to_visit(url)
        with open("m.txt", "a") as f: 
         rake_nltk_var.extract_keywords_from_text(self.find_meta(url, html))
         keyword_extracted = rake_nltk_var.get_ranked_phrases()
         print(url)
         f.write(
					 json.dumps({"kwd": ((keyword_extracted)), "url": url2})+","
					 )	
					 

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://www.worldcubeassociation.org']).run()
