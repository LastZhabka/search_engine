import requests
from bs4 import BeautifulSoup
from queue import Queue
from urllib.parse import urljoin
import sys, os
sys.path.append(os.getcwd())
from core.search_engine.database.crawlerStorage import URLQueue, URLsGraph, URLStorage, Logger

#utilities
def standartize_url(url):
    while len(url) and url[-1] == '/':
        url = url[0:-1]
    if "#" in url:
        url = url[0:url.find("#")]
    if "?" in url:
        url = url[0:url.find("?")]
    return url

def is_incorrect_url(url):
    if ('.jpg' in url) or ('.png' in url) or ('.JPG' in url) or ('.PNG' in url):
        return True
    if not (".hk" in url):
        return True
    if not ("ust" in url):
        return True
    if "news" in url:
        return True
    if "download" in url:
        return True
    #if not (("prog-crs" in url) or ("prog_crs" in url) or ("ugadmin" in url)):
    #    return True
    if not url.startswith("http"):
        return True
    return False

def is_pdf(url):
    return (len(url) > 3) and (url[-4:] == ".pdf")

def get_response_type(response):
    return response.headers['Content-Type'].split('/')[1][:4]

def url_preproc(url1, url2):
    try:
        result = standartize_url(urljoin(url1, url2)) 
        if is_incorrect_url(result):
            return ""
        return result
    except:
        return ""

class WebCrawler:
    def __init__(self, indexingCallback):
        self.unprocessed_urls = URLQueue()
        self.urls_graph = URLsGraph()
        self.urls = URLStorage()
        self.logger = Logger()
        self.indexingCallback = indexingCallback

    def propagate_from_url(self, url, links):
        for link in links:
            next_url = url_preproc(url, link.get("href"))
            if len(next_url) > 0:
                self.urls_graph.connect_urls(next_url, url)
                if self.urls.is_visited(next_url):
                    continue
                self.urls.add_url(next_url)
                self.unprocessed_urls.push_url(next_url)

    def crawl_url(self, url):
        try:
            response = requests.get(url)
        except:
            return
        response_type = get_response_type(response)
        if response_type == 'html' or response_type == 'pdf':
            self.indexingCallback(responseContent=response.content, format=response_type, url=url)
        if response_type == 'html':      
            soup = BeautifulSoup(response.content, "html.parser")
            self.propagate_from_url(url, soup.find_all('a'))

    def start_crawling(self, ):
        while not self.unprocessed_urls.is_empty():
            url = self.unprocessed_urls.get_url()['url']
            self.crawl_url(url)
            print("Crawled : ", url)



