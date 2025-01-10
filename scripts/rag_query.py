import sys, os
sys.path.append(os.getcwd())
from core.rag_pipeline.rag_pipeline import RAGPipeline


# set api key in core.rag_pipeline.rag_pipeline.api_key.txt
x = RAGPipeline()
input = "..."

x.ask(input)