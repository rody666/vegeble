from openai import OpenAI
from api_key import apikey
import base64
# クライアントを作成
client = OpenAI(api_key=apikey.api_key)

response = client.responses.create(
    model="gpt-5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)