import pyttsx3
import time

print("Initializing engine...")
init_start = time.time()
engine = pyttsx3.init()
engine.setProperty('rate', 175)
init_end = time.time()
print(f"Init time: {init_end - init_start:.2f} seconds")

text = "Hi there!?"

print("Speaking...")
speak_start = time.time()
engine.say(text)
engine.runAndWait()
speak_end = time.time()

print(f"Speak time: {speak_end - speak_start:.2f} seconds")