import os
import time
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from groq import Groq
import pyttsx3

load_dotenv()

# --- Initialize everything ONCE at startup ---
print("Loading models... please wait")
stt_model = WhisperModel("small", device="cpu", compute_type="int8")
llm_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 175)
print("Ready!")

sample_rate = 16000
duration = 5  # seconds to record each turn

def record_audio():
    print("\n🎤 Listening... speak now!")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    return recording.flatten()

def transcribe(audio):
    segments, info = stt_model.transcribe(audio, language="en")
    text = " ".join([seg.text for seg in segments]).strip()
    return text

def get_llm_reply(user_text):
    response = llm_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful, friendly voice assistant. Keep answers short and conversational, 2-3 sentences max."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# --- Main loop ---
while True:
    audio = record_audio()

    t0 = time.time()
    user_text = transcribe(audio)
    t1 = time.time()

    if not user_text:
        print("(Didn't catch anything, try again)")
        continue

    print(f"You said: {user_text}  [STT: {t1-t0:.2f}s]")

    t2 = time.time()
    reply = get_llm_reply(user_text)
    t3 = time.time()

    print(f"Assistant: {reply}  [LLM: {t3-t2:.2f}s]")
    print(f"Time to first response (STT+LLM): {t3-t0:.2f}s")

    speak(reply)

    print("\n(Say 'stop' or press Ctrl+C to end)")
    if "stop" in user_text.lower():
        print("Goodbye!")
        break