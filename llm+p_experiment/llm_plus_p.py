from openai import OpenAI
import os
from prompt_creater import prompt_creater

openai_api_key = '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'

def llm_plus_p_function(query):
    prompt = prompt_creater(query)

    client = OpenAI(
        # This is the default and can be omitted
        api_key=openai_api_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": prompt}
    #     ]
    # )

    return response.choices[0].message.content

