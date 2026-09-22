from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(timeout=60)

response = client.responses.create(
    model="gpt-5",
    input="Réponds uniquement par le mot Bonjour."
)

print(response.output_text)
