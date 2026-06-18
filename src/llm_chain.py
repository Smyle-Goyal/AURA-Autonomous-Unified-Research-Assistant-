from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OpenRouterKey"),
)

SYSTEM_PROMPT = """You are AURA, an expert research assistant specialized in analyzing academic papers.

YOUR CORE RULES:
1. Answer ONLY from the provided context chunks. Never use outside knowledge.
2. Be SHORT and DIRECT. No fluff, no repetition.
3. ALWAYS cite your source at the end of every claim as (Source: filename, Page X).
4. If multiple chunks support the answer, cite all of them.
5. If the answer is NOT in the context, respond exactly with:
   "This information is not present in the uploaded paper. Try asking about: [suggest 2-3 relevant topics based on the context you do have]"
6. If the question is vague, answer the most likely interpretation directly.
7. Never say "based on the context" or "according to the document" — just answer directly and cite.
8. If asked to summarize, give a 3-5 sentence summary with citations.

YOUR RESPONSE FORMAT:
- Direct answer in 2-4 sentences max
- Citations inline or at end: (Source: filename, Page X)
- If multiple points needed, use a short numbered list
- No long introductions, no "Great question!", no filler phrases
"""

def build_context(retrieved_chunks):
    """Formats retrieved chunks into a clean numbered context block."""
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        source = chunk.metadata.get("source", "Unknown")
        page = chunk.metadata.get("page", "?")
        context += f"\n--- Chunk {i+1} | Source: {source} | Page {page} ---\n"
        context += f"{chunk.page_content.strip()}\n"
    return context

def generate_answer(question, retrieved_chunks):
    """Generate a cited answer from retrieved chunks using OpenRouter."""

    context = build_context(retrieved_chunks)

    user_message = f"""CONTEXT FROM PAPER:
{context}

QUESTION: {question}

Answer directly and concisely. Cite every claim."""

    # Retry up to 3 times on rate limit
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content

        except Exception as e:
            if "429" in str(e):
                wait = (attempt + 1) * 10
                print(f"Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise e

    return "AURA is currently busy. Please try again in a moment."