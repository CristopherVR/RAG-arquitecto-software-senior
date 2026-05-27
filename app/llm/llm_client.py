from groq import Groq
from app.config import GROQ_API_KEY, LLM_MODEL


class LLMClient:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = LLM_MODEL

    def generate(self, system_prompt, user_prompt):
        """
        Envía un prompt al LLM y retorna la respuesta como string.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.2,      # Baja temperatura = respuestas más precisas y menos alucinaciones
            max_tokens=2048,
        )

        return response.choices[0].message.content