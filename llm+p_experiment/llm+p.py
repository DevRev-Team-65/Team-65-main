import openai
import os
from prompt_creater import prompt_creater

openai.api_key_path = 'openai_key.txt'

query = input("query: ")
prompt = prompt_creater(query)

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
      {"role": "system", "content": prompt}
  ]
)

print(response['choices'][0]['message']['content'])