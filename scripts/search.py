import sys, os
sys.path.append(os.getcwd())
from core.search_engine.search_engine import SearchEngine

x = SearchEngine()
queryText = "icpc"
print(x.get(queryText)['urls']) # TODO