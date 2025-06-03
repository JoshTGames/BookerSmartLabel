import sys, pyaudio, threading, multiprocessing
from queue import Queue as q
from vosk import Model, KaldiRecognizer

class SpeechRecognition:
    RATE = 16000
    CHUNK = 1024
    MODEL_PATH = "vosk-model-small-en-us-0.15"

    def __init__(self):
        self.model = Model(SpeechRecognition.MODEL_PATH)
        self.recogniser = 

        self.data = q()

    def listener(self):
        """"""
        