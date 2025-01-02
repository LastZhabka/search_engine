
from urllib.parse import urljoin

class URLProcessor:
    def __init__(self,):
        pass

    def standartizeURL(self, url):
        while len(url) and url[-1] == '/':
            url = url[0:-1]
        if "#" in url:
            url = url[0:url.find("#")]
        if "?" in url:
            url = url[0:url.find("?")]
        return url

    def isIncorrectURL(self, url):
        if ('.jpg' in url) or ('.png' in url) or ('.JPG' in url) or ('.PNG' in url):
            return True
        if ('.zip' in url) or ('.pptx' in url) or ('.mp4' in url) or ('.mp3' in url):
            return True
        if (not (".hk" in url)) or (not ("ust" in url)) or (not url.startswith("http")):
            return True
        if ("news" in url) or ("download" in url):
            return True
        #if not (("prog-crs" in url) or ("prog_crs" in url) or ("ugadmin" in url)):
        #    return True
        return False

    def getResponseType(self, response):
        return response.headers['Content-Type'].split('/')[1][:4]

    def joinURLs(self, url1, url2):
        try:
            result = self.standartizeURL(urljoin(url1, url2)) 
            if self.isIncorrectURL(result):
                return "" # empty string indicates that url is incorrect
            return result
        except:
            return ""