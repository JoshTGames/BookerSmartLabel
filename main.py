import command_handler, screen as s#, speech_recog as sr
MANAGER : command_handler.CommandHandler = command_handler.CommandHandler()
SCREEN : s.Screen = s.Screen()
import ovos_classifiers
# SPEECH : sr.SpeechRecognition = sr.SpeechRecognition()

# Start thread for speech recog...

# CMDLINE
while True:
    print(dir(ovos_classifiers))
    cmd = str(input("Command:\t")).split()
    MANAGER.execute(cmd[0], *cmd[1:])

# import sys, os, time


# libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

# from lib import screen

# import sounddevice as sd
# import queue
# import json
# from vosk import Model, KaldiRecognizer

# # Load Vosk Model
# model_path = "vosk-model-small-en-us-0.15"
# model = Model(model_path)
# recognizer = KaldiRecognizer(model, 16000)

# # Create an audio queue
# q = queue.Queue()

# # Callback function for audio recording
# def callback(indata, frames, time, status):
#     if status:
#         print(status, flush=True)
#     q.put(indata[:])

# try:
#     with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
#         print("Listening... Speak now.")
#         while True:
#             data = q.get()
#             if recognizer.AcceptWaveform(data):
#                 result = json.loads(recognizer.Result())                
#                 print("You said:", result["text"])

# except KeyboardInterrupt:
#     screen.epd2in13_V4.epdconfig.module_exit(cleanup=True)
#     exit()