from nltk.tokenize import sent_tokenize, word_tokenize 
from bs4 import BeautifulSoup
import PyPDF2
import io
from nltk.corpus import stopwords
from abc import ABC, abstractmethod
from functools import reduce

def retrievePDFText(responseContent):
    file = PyPDF2.PdfReader(io.BytesIO(responseContent))
    textContent = []
    for page_num in range(len(file.pages)):
        page = file.pages[page_num].extract_text().split('\n')
        for text in page:
            if len(textContent) == 0 or len(text)  == 0 or text[0] < 'a':
                textContent.append(text)
            else:
                textContent[len(textContent) - 1] += text
    return textContent

def retrieveHTMLText(responseСontent):
    return BeautifulSoup(responseСontent, "html.parser").get_text(separator = " # ", strip = True).split(" # ")

class Tokenizer(ABC):
    @abstractmethod
    def __init__(self, ):
        pass

    @abstractmethod
    def getTokens(self, text):
        pass
    
    def getTokensFromResponse(self, responseContent, format):
        match format:
            case "pdf":
                text = retrievePDFText(responseContent)
            case "html":
                text = retrieveHTMLText(responseContent)
        return self.getTokens(text)

class WordTokenizer(Tokenizer):
    def __init__(self, ):
        self.english_stopwords = set(stopwords.words('english'))
        self.extra_stopchars = r'[&^%$#@!*()_+\-=\[\]{};:"\\|,.<>\/?]'
    
    def isValid(self, word):
        if word in self.extra_stopchars or word in self.extra_stopchars:
            return False
        for char in word:
            if '\u4e00' <= char <= '\u9fff': #chinese symbols
                return False
        return True

    def getTokens(self, text):
        words = []
        for subtext in text:
            words = words + list(filter(self.isValid, word_tokenize(subtext.lower())))
        return words

class TextBatchTokenizer(Tokenizer):
    def __init__(self,):
        self.batchSize = 350
    
    def getTokens(self, text):
        sentences = reduce(lambda acc, x: acc + x, [sent_tokenize(subtext) for subtext in text], [])
        batches = [""]
        for sentence in sentences:
            if len(batches[-1]) + len(sentence) <= self.batchSize:
                batches[-1] = batches[-1] + sentence
            else:
                batches.append(sentence)
        return batches