from functions import FunctionInterface
from myopenai import OpenAIHandler

from devrev import devrev_functions
from config import llama_token, llama_base, llama_model

handler = OpenAIHandler(
    api_base=llama_base,
    api_key=llama_token,
    functions=devrev_functions,
    model=llama_model
)

if __name__ == '__main__':
    while True:
        message = input('You: ')
        response = handler.query(message)
        print('Llama: \n', response)