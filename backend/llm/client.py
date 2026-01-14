import os
from groq import Groq
from dotenv import load_dotenv

from backend.llm.prompts import SYSTEM_PROMPT
from backend.llm.tools_schema import TOOLS

load_dotenv()

def call_llm(messages):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    client = Groq(api_key=api_key)

    return client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *messages
        ],
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.2,
    )

