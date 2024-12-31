from nltk.tokenize import sent_tokenize, word_tokenize 
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from abc import ABC, abstractmethod
from functools import reduce
import time



class Tokenizer(ABC):
    @abstractmethod
    def __init__(self, ):
        pass

    @abstractmethod
    def getTokens(self, text):
        pass

class WordTokenizer(Tokenizer):
    def __init__(self, ):
        self.porterStemmer = PorterStemmer()
        self.englishStopwords = set(stopwords.words('english'))
        self.extraStopchars = r'[&^%$#@!*()_+\-=\[\]{};:"\\|,.<>\/?]'
    
    def isValid(self, word):
        if word in self.extraStopchars or word in self.englishStopwords:
            return False
        for char in word:
            if '\u4e00' <= char <= '\u9fff': #chinese symbols
                return False
        return True

    def getTokens(self, text):
        words = []
        for subtext in text:
            words = words + list(filter(self.isValid, word_tokenize(subtext.lower())))
        words = [self.porterStemmer.stem(word) for word in words] # add stemming
        return words

class TextBatchTokenizer(Tokenizer):
    def __init__(self, batchSize = 350):
        self.batchSize = batchSize
    
    def getTokens(self, text):
        sentences = reduce(lambda acc, x: acc + x, [sent_tokenize(subtext) for subtext in text], [])
        batches = [""]
        for sentence in sentences:
            if len(batches[-1]) + len(sentence) <= self.batchSize:
                batches[-1] = batches[-1] + sentence + "\n"
            else:
                batches.append(sentence)
        return batches