import openai
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--query", default=None, type=str, required=True, help="Enter your query: ")
parser.add_argument("--api_key", default=None, type=str, required=True, help="Enter your OpenAI API key: ")
args = parser.parse_args()
openai.api_key = args.api_key

from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_str = f"""Retrieve only the necessary tools required to answer the following query:
{args.query}
 If the query cannot be answered by the existing tools givee an empty list as your answer. If the query can be answered then only retrieve the tools necessary to answer the query"""

query_engine = index.as_query_engine()
response = query_engine.query(query_str)
print(response)
