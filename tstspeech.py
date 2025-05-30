# import speech_recognition as sr

# recognizer = sr.Recognizer()

# # Select the correct microphone (usually index 0)
# with sr.Microphone(device_index=0) as source:
#     print("Listening... Speak now.")
#     recognizer.adjust_for_ambient_noise(source)
#     audio = recognizer.listen(source)

# try:
#     text = recognizer.recognize_google(audio)
#     print("You said:", text)
# except sr.UnknownValueError:
#     print("Sorry, I couldn't understand that.\t")
# except sr.RequestError:
#     print("Could not request results from Google Speech Recognition service.")

import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# Load Vosk Model
model_path = "vosk-model-small-en-us-0.15"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Create an audio queue
q = queue.Queue()

# Callback function for audio recording
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(indata[:])

# Start the microphone stream
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="float32",
                       channels=1, callback=callback):
    print("Listening... Speak now.")

    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("You said:", result["text"])
