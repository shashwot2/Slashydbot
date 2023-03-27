import os
import openai
from dotenv import load_dotenv

load_dotenv()


async def chatgpt(prompt, persona):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt},
        ],
        max_tokens=175,
        n=1,
        temperature=0.8,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    message = completions["choices"][0]["message"]["content"]
    return message
