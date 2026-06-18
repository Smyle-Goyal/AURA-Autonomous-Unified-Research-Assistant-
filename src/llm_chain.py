from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OpenRouterKey"),
)


def generate_answer(question, retrieved_chunks):
    """Generate an answer from retrieved chunks using OpenRouter."""
    
    # Build context from chunks with citations
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        source = chunk.metadata.get("source", "Unknown")
        page = chunk.metadata.get("page", "?")
        context += f"\n[{i+1}] (Source: {source}, Page {page})\n{chunk.page_content}\n"

    prompt = f"""You are a research assistant. Answer the question using ONLY the context below.
Always cite your sources as (Source: filename, Page X).
If the answer isn't in the context, say "I couldn't find this in the uploaded papers."

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content