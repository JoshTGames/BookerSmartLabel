import sys, os, time, sounddevice as sd

from queue import Queue as Q
from threading import Thread
from vosk import Model, KaldiRecognizer

import json_manager as j
from screen import Screen as s
from command_handler import CommandHandler as ch


class SpeechRecognition:
    RATE = 16000
    CHUNK = 1024
    MODEL_PATH = "vosk-model-small-en-us-0.15"


    def __init__(self):
        self.data = Q()
        self.settings = j.read_file(os.getcwd() + '/settings.json')['speech']

        # Runs the listener on a separate thread
        listen_thread = Thread(target=self.__listener, daemon=True)
        listen_thread.start()

        recognition_thread = Thread(target=self.__process, daemon=True)
        recognition_thread.start()

    def __listener(self):
        """Collects data from microphone & enters it into a queue"""
        def callback(indata, _, __, ___):
            self.data.put(indata[:])

        with sd.RawInputStream(SpeechRecognition.RATE, blocksize=SpeechRecognition.CHUNK, dtype="int16", channels=1, callback=callback):
            while True:
                time.sleep(0.1)

    def __process(self):
        model = Model(SpeechRecognition.MODEL_PATH)
        recogniser = KaldiRecognizer(model, SpeechRecognition.RATE) 
        
        wakeword = self.settings['wake-word']
        wake_detected = False # If true, start listening
        

        while True:
            data = self.data.get(block=True)
            if recogniser.AcceptWaveform(data):
                rslt = recogniser.Result()
                text = rslt.split('"')[3]


                if not wake_detected and wakeword in text.lower():
                    # CHANGE SCREEN TO LISTENING
                    s.instance.set_text(0, ("Listening...", "h2", "center"))
                    wake_detected = True
                    continue

                if wake_detected:
                    print(f"Recognised: {text}")
                    message = text.split()
                    print(message)
                    ch.instance.execute(message[0], message[1:])
                    wake_detected = False