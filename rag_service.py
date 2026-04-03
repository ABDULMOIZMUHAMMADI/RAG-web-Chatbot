import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def split_text(text, chunk_size=400):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def generate_answer(context, question):

    prompt = f"""
Context:
{context}

Question:
{question}

Answer only using the context above.
"""

    response = model.generate_content(prompt)

    return response.text