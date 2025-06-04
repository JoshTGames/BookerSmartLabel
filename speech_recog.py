import sys, os, time, sounddevice as sd

from queue import Queue as Q
from threading import Thread
from vosk import Model, KaldiRecognizer

import json_manager as j
from screen import Screen as s
from command_handler import CommandHandler
from timer import Timer as t


class SpeechRecognition:
    RATE = 16000
    CHUNK = 1024
    MODEL_PATH = "vosk-model-small-en-us-0.15"


    def __init__(self, ch: CommandHandler):
        self.data = Q()
        self.settings = j.read_file(os.getcwd() + '/settings.json')['speech']

        self.model = Model(SpeechRecognition.MODEL_PATH)
        self.recogniser = KaldiRecognizer(self.model, SpeechRecognition.RATE) 
        self.ch = ch
        
        self.wakeword = self.settings['wake-word']
        self.wake_detected = False # If true, start listening

        # Runs the listener on a separate thread
        listen_thread = Thread(target=self.__listener, daemon=True)
        listen_thread.start()

        recognition_thread = Thread(target=self.__process, daemon=True)
        recognition_thread.start()

    def __listener(self):
        """Collects data from microphone & enters it into a queue"""
        def callback(indata, _, __, status):
            if status:
                print(status, flush=True)
            self.data.put(indata[:])

        with sd.RawInputStream(SpeechRecognition.RATE, blocksize=SpeechRecognition.CHUNK, dtype="int16", channels=1, callback=callback):
            while True:
                time.sleep(0.1)

    def __process(self):
        
        

        while True:
            data = self.data.get(block=True)
            if self.recogniser.AcceptWaveform(data):
                rslt = self.recogniser.Result()
                text = rslt.split('"')[3]


                if not self.wake_detected and self.wakeword in text.lower():
                    # CHANGE SCREEN TO LISTENING
                    s.instance.set_text(0, ("Listening...", "h2", "center"))
                    print("Listening!")
                    t.instance.stop()
                    self.wake_detected = True
                    continue

                if self.wake_detected:
                    print(f"Recognised: {text}")
                    message = text.split()
                    self.ch.execute(message[0], *message[1:])
                    self.wake_detected = False