import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


PROMPT = """
You are a Medical Device QA Engineer.

Generate exactly 5 QA test cases.

Return ONLY valid JSON.

Format:

{
  "test_cases":[
      {
          "title":"",
          "steps":"",
          "expected_result":""
      }
  ]
}
"""


def generate_test_cases(text: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)