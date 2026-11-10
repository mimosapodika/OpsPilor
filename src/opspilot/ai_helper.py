import os
import streamlit as st
from groq import Groq

def get_groq_client():
    """Configure and return Groq client if API key is available."""
    # First check environment variables (used by FastAPI backend)
    api_key = os.getenv("GROQ_API_KEY", "")

    # Fallback to Streamlit secrets if running inside Streamlit
    if not api_key:
        try:
            api_key = st.secrets["groq"]["api_key"]
        except (FileNotFoundError, KeyError, Exception):
            pass

    if api_key:
        return Groq(api_key=api_key)
    return None

def analyze_ticket_with_ai(description: str) -> dict:
    """
    Sends the ticket description to Groq (Llama 3.3) to generate
    an AI-powered troubleshooting insight and triage recommendation.
    """
    client = get_groq_client()
    if not client:
        return {"ai_analysis": "Groq API key not configured. Set GROQ_API_KEY in your environment."}

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert IT support assistant. Provide concise, professional 1-2 sentence troubleshooting steps or resolution guides for IT admins."
                },
                {
                    "role": "user",
                    "content": f"Analyze this IT support ticket description: '{description}'"
                }
            ],
            temperature=0.3,
            max_tokens=200
        )

        analysis_text = completion.choices[0].message.content.strip()
        return {"ai_analysis": analysis_text}

    except Exception as e:
        return {"ai_analysis": f"Groq AI processing error: {str(e)}"}
