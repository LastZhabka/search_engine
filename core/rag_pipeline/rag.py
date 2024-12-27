"""
THRASH CODE, JUST TESTED ANOTHER PART, IGNORE IT FOR NOW.

"""


"""
DOCUMENT:
(document text)

QUESTION:
(users question)

INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return {NONE}
"""
import sys, os
sys.path.append(os.getcwd())
from core.search_engine.indexing_pipeline.tokenizer.tokenizer import TextBatchTokenizer, WordTokenizer
import requests
from datetime import datetime
def get_response_type(response):
    return response.headers['Content-Type'].split('/')[1][:4]


def timeCounter(func):
    def func_2(*args, **kwargs):
        tim = datetime.now()
        x = func(*args, **kwargs)
        print(datetime.now() - tim)
        return x
    return func_2

@timeCounter
def getContent(url):
    print(url)
    import time
    try:
        t__ = time.time()
        response = requests.get(url)
        print(f"Response : {time.time() - t__}")
    except:
        return ['']
    
    responseType = get_response_type(response)
    t0 = time.time()
    tokens2 = WordTokenizer().getTokensFromResponse(response.content, responseType)
    print(f"Word Tokenization : {time.time() - t0}")
    t0 = time.time()
    tokens = TextBatchTokenizer(batchSize=500).getTokensFromResponse(response.content, responseType)
    print(f"Text Batch Tokenization : {time.time() - t0}")
    return tokens
    
    
        
size = 0
sz = 0
for content in getContent("https://publications.ust.hk/Annual_Report/2015-2016/eng/annual_report_1516.pdf"):
    size += len(content)
    sz += 1

print(sz)
print(size)