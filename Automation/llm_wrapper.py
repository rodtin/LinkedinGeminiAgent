import os
import google.generativeai as genai
from openai import OpenAI

# Usage:
# response_text = generate_llm_response(prompt)

def generate_llm_response(prompt: str) -> str:
    """
    Generates content using the configured LLM provider (Gemini or OpenAI).
    Automatically falls back to OpenAI if Gemini fails (e.g. Quota Exceeded).
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    # Internal function to call OpenAI
    def call_openai():
        print("🔄 Switching to OpenAI...")
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found during fallback.")
            
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # If explicitly set to openai, just do that
    if provider == "openai":
        return call_openai()

    # Default / Gemini
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"⚠️ Gemini Error: {e}")
        # Check for Quota/ResourceExhausted or just generic fallback
        # In this simple implementation, we fallback on ANY Gemini failure
        print("⚠️ Falling back to OpenAI...")
        return call_openai()
