import sys, os
sys.path.append(os.getcwd())
from core.rag_pipeline.rag_pipeline import RAGPipeline


# set api key in core.rag_pipeline.rag_pipeline.api_key.txt

x = RAGPipeline()
input = "Who participated in ICPC EC Final 2023 ?"
x.ask(input)
"""
**Question:**
Who participated in ICPC EC Final 2023 ?

**Answer:**
Based on the document provided, the members of Team 1 who participated in the ICPC Asia East Continent Final Contest in 2023 are Ka Kit Lui, Sin Hang Yeung, and Tsz Fung Wong. Team 2 also participated in the same contest, consisting of Taimas Korganbayev, Mukhammadarif 
Sakhmoldin, and Raiymbek Baishuak.
"""