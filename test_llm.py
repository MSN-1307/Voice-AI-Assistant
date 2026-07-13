import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

user_text = "Tell me a fun fact about space."

print("Sending to LLM...")
start = time.time()

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a helpful, friendly voice assistant. Keep answers short and conversational, 2-3 sentences max."},
        {"role": "user", "content": user_text}
    ]
)

end = time.time()

reply = response.choices[0].message.content
print("LLM reply:", reply)
print(f"Time taken: {end - start:.2f} seconds")