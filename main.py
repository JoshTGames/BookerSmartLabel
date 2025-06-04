import command_handler, screen as s, speech_recog as sr
from timer import Timer
import os, time, json_manager



MANAGER : command_handler.CommandHandler = command_handler.CommandHandler()
SPEECH : sr.SpeechRecognition = sr.SpeechRecognition(MANAGER)
SCREEN : s.Screen = s.Screen()
TIMER : Timer = Timer(json_manager.read_file(f'{os.getcwd()}/settings.json')['screen-timer'], s.instance.set_default)

# CMDLINE

# DOESNT WORK IN SYSTEMCTL
while True:
    time.sleep(1)
#     cmd = str(input("Command:\t")).split()
#     if(len(cmd) <= 0): continue
#     MANAGER.execute(cmd[0], *cmd[1:])
