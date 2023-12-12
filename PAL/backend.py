# Copyright 2022 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import openai
import time
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

# GPT-3 API
def call_gpt(prompt, model='gpt-3.5-turbo', stop=None, temperature=0., top_p=1.0,
             max_tokens=128, majority_at=None):
  num_completions = majority_at if majority_at is not None else 1
  num_completions_batch_size = 5

  completions = []
  for i in range(20 * (num_completions // num_completions_batch_size + 1)):
    try:
      requested_completions = min(num_completions_batch_size, num_completions - len(completions))
      if model in ['gpt-4', 'gpt-3.5-turbo']:
        ans = chat_api(
            model=model,
            max_tokens=max_tokens,
            stop=stop,
            prompt=prompt,
            temperature=temperature,
            top_p=top_p,
            n=requested_completions,
            best_of=requested_completions)
      else:
        ans = completions_api(
            model=model,
            max_tokens=max_tokens,
            stop=stop,
            prompt=prompt,
            temperature=temperature,
            top_p=top_p,
            n=requested_completions,
            best_of=requested_completions)
      completions.extend(ans)
      if len(completions) >= num_completions:
        return completions[:num_completions]
    except openai.error.RateLimitError as e:
      time.sleep(min(i**2, 60))
  raise RuntimeError('Failed to call GPT API')

def completions_api(model, max_tokens, stop, prompt, temperature,
            top_p, n, best_of):
    ans = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        stop=stop,
        prompt=prompt,
        temperature=temperature,
        top_p=top_p,
        n=n,
        best_of=best_of
    )
    return ans.choices[0]['text'] if ans.choices else ""


def chat_api(model, max_tokens, stop, prompt, temperature, top_p, n, best_of):
    ans = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        stop=stop,
        prompt=prompt,
        temperature=temperature,
        top_p=top_p,
        n=n,
        best_of=best_of,
        return_prompt=True  
    )
    completion_text = ans.choices[0]['text'] if ans.choices else ""
    schema = generate_json_schema(completion_text)
    
    return schema 

def generate_json_schema(query):
    prompt = f"Generate a JSON schema for: {query}"
    model = 'gpt-3.5-turbo'
    stop = None
    temperature = 0.0
    top_p = 1.0
    max_tokens = 512 
    completions = call_gpt(prompt, model=model, stop=stop, temperature=temperature,
                           top_p=top_p, max_tokens=max_tokens)
    
    schema = completions[0] if completions else "No schema generated."
    return schema


def call_chat_gpt(messages, model='gpt-3.5-turbo', stop=None, temperature=0., top_p=1.0, max_tokens=128):
  wait = 1
  while True:
    try:
      ans = openai.ChatCompletion.create(
          model=model,
          max_tokens=512,
          messages=messages,
          temperature=0.0,
          top_p=0.0,
          n=1
      )
      return ans.choices[0]['message']['content']
    except openai.error.RateLimitError as e:
      time.sleep(min(wait, 60))
      wait *= 2
    except openai.error.InvalidRequestError as e:
      if "This is a chat model and not supported in the v1/completions endpoint" in str(e):
        raise openai.error.InvalidRequestError(
            "This is a chat model and not supported in the v1/completions endpoint. Use v1/chat/completions."
        ) from None
      else:
        raise e
  raise RuntimeError('Failed to call chat gpt')
