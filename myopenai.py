import openai
import json

class OpenAIHandler:
    def __init__( self, api_base: str, api_key: str, functions: list, model: str = 'llama-13b-chat' ):
        openai.api_base = api_base
        openai.api_key = api_key
        self.functions = functions
        self.model = model
        self.history = []

    def query(self, message):
        self.history.append(
            {"role":"user", "content":message}
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
            functions=self.functions
        )
        message = response['choices'][0]['message']
        finish_reason = response['choices'][0]['finish_reason']
        if finish_reason == 'function_call':
            # this is the end of the conversation
            function_call = message['function_call']
            #convert string to json for function arguments
            # f_args = json.loads(function_call['arguments'])
            self.history.append({"role": "assistant", "function_call": function_call})
            return function_call
        else:
            # this is not yet the end of the conversation
            content = message['content']
            self.history.append({"role": "assistant", "content": content})
            return content