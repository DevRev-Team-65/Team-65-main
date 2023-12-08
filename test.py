from openai_retrievers import CustomMultiQueryRetriever
from prompting import ChainOfThoughtComposer
from config import openai_key
from functions import devrev_functions

# Create the retriever
retriever = CustomMultiQueryRetriever(
    openai_key=openai_key,
    name="cmqr_vs_1",
    init_functions=devrev_functions
)

# Create the composer
composer = ChainOfThoughtComposer(
    openai_api_key=openai_key,
    temperature=0.0,
    max_tokens=1000,
)

if __name__ == '__main__':
    while True:
        query = input('Enter a query: ')
        functions = retriever.find_functions(query)
        answer = composer(query=query, functions=functions)
        print(answer)