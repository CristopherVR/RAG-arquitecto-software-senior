from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Embedder:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_embedding(self, text):

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding