import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

duration = 4
sample_rate = 16000

print("Loading Whisper model... (first time will download it, may take a minute)")
model = WhisperModel("small", device="cpu", compute_type="int8")

print("Recording for 4 seconds... speak now!")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
sd.wait()
print("Recording done. Transcribing...")

audio = recording.flatten()
segments, info = model.transcribe(audio, language="en")

print("You said:")
for segment in segments:
    print(segment.text)