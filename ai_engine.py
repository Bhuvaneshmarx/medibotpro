import os
from openai import OpenAI

# Get API key from environment variable in cloud
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

SYSTEM_PROMPT = """
You are MediBot Pro, an AI health information assistant.

Rules:
- You provide general medical information only.
- You are NOT a real doctor.
- Do NOT diagnose or prescribe exact medicines by brand name.
- Encourage users to see a real doctor for diagnosis and treatment.
- If user describes emergency symptoms (e.g., chest pain, trouble breathing, severe bleeding, unconsciousness),
  advise them to seek IMMEDIATE emergency medical help or call their local emergency number.
- Keep answers simple, clear, and under 200–250 words unless user asks for more detail.
- Always answer in the language the user requests.
"""

class MediAI:
    def __init__(self, api_key=None, model="gpt-4.1-mini"):
        key = (api_key or API_KEY).strip()
        if not key or "sk-" not in key:
            raise ValueError(
                "❌ OpenAI API key is missing. "
                "Set environment variable OPENAI_API_KEY on the server."
            )

        print("✅ MediAI: Initializing OpenAI client...")
        self.client = OpenAI(api_key=key)
        self.model = model
        print("✅ MediAI: Ready.")

    def get_response(self, user_text, language_name="English"):
        try:
            user_prompt = (
                f"User preferred language: {language_name}.\n"
                f"Answer ONLY in this language.\n"
                f"User question: {user_text}"
            )

            chat = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )

            return chat.choices[0].message.content.strip()

        except Exception as e:
            print("❌ Error:", e)
            return f"Error: {e}"
