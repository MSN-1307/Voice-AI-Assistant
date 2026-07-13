import sounddevice as sd
import numpy as np

duration = 4  # seconds
sample_rate = 16000

print("Recording for 4 seconds... speak now!")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
sd.wait()
print("Recording done. Playing it back...")

sd.play(recording, samplerate=sample_rate)
sd.wait()
print("Playback done. If you heard yourself, mic + speakers work!")