import sys, os
sys.path.append(os.getcwd())
from core.rag_pipeline.rag_pipeline import RAGPipeline


# set api key in core.rag_pipeline.rag_pipeline.api_key.txt

x = RAGPipeline()
input = "Who participated in ICPC ?(People names)"
x.ask(input)
"""
**Question:**
Who participated in ICPC ?(People names)

**Answer:**
The people who participated in the ICPC (International Collegiate Programming Contest) as 
mentioned in the document are:

- Team 1 members: Ka Kit Lui, Sin Hang Yeung, Tsz Fung Wong
- Team 2 members: Taimas Korganbayev, Mukhammadarif Sakhmoldin, Raiymbek Baishuak

Therefore, the individuals who participated in the ICPC from the document are Ka Kit Lui, 
Sin Hang Yeung, Tsz Fung Wong, Taimas Korganbayev, Mukhammadarif Sakhmoldin, and Raiymbek 
Baishuak.
"""