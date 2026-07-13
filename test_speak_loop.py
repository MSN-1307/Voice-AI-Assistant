import pyttsx3

def speak(text):
    local_engine = pyttsx3.init()
    local_engine.setProperty('rate', 175)
    local_engine.say(text)
    local_engine.runAndWait()
    local_engine.stop()
    del local_engine

print("Saying first phrase...")
speak("This is the first test.")

print("Saying second phrase...")
speak("This is the second test.")

print("Saying third phrase...")
speak("This is the third test.")

print("Done.")