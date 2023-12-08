from openai_retrievers import CustomMultiQueryRetriever
from prompting import ChainOfThoughtComposer
from config import openai_key
from functions import devrev_functions

# Create the retriever
retriever = CustomMultiQueryRetriever(openai_key)

# Add the functions to the retriever
retriever.add_functions(devrev_functions)

# Create the composer
composer = ChainOfThoughtComposer(
    openai_api_key=openai_key,
    temperature=0.0,
    max_tokens=1000,
)

def get_answer(query: str):
    # Get the relevant functions
    functions = retriever.find_functions(query)
    # Run the composer
    answer = composer(query=query, functions=functions)
    # and return it : )
    return answer

if __name__ == '__main__':
    while True:
        query = input('Enter a query: ')
        print(get_answer(query))