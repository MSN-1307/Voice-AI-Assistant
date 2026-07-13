import os
import time
import random
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
print("Ready!")

sample_rate = 16000
duration = 5  # seconds to record each turn

FILLERS = [
    "Let me think about that for a moment.",
    "Good question, give me a moment.",
    "Hmm, let me work that out.",
    "One moment, thinking it through.",
]

conversation_history = [
    {"role": "system", "content": "You are a helpful, friendly voice assistant. Keep answers short and conversational, 2-3 sentences max."}
]


def record_audio():
    print("\n🎤 Listening... speak now!")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    return recording.flatten()


def transcribe(audio):
    segments, info = stt_model.transcribe(
        audio,
        language="en",
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        initial_prompt="This is a casual conversation. The speaker's name is Saini Kitmalisetti.",
    )
    text = " ".join([seg.text for seg in segments]).strip()
    return text


def get_llm_reply(user_text):
    conversation_history.append({"role": "user", "content": user_text})

    response = llm_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation_history
    )
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})

    if len(conversation_history) > 21:
        conversation_history[:] = [conversation_history[0]] + conversation_history[-20:]

    return reply


def speak(text):
    local_engine = pyttsx3.init()
    local_engine.setProperty('rate', 175)
    local_engine.say(text)
    local_engine.runAndWait()
    local_engine.stop()


def main():
    while True:
        audio = record_audio()

        # Immediately acknowledge so the user is never left in silence
        speak(random.choice(FILLERS))

        t0 = time.time()
        user_text = transcribe(audio)
        t1 = time.time()

        if not user_text:
            print("(Didn't catch anything clearly, let's try again)")
            speak("Sorry, I didn't quite catch that. Could you say it again?")
            continue

        reply = get_llm_reply(user_text)
        t2 = time.time()

        print(f"You said: {user_text}  [STT: {t1-t0:.2f}s]")
        print(f"Assistant: {reply}  [LLM: {t2-t1:.2f}s]")

        speak(reply)

        print("\n(Say 'stop' to end)")
        if "stop" in user_text.lower():
            speak("Goodbye!")
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()