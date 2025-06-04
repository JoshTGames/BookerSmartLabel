import command_handler, screen as s, speech_recog as sr
MANAGER : command_handler.CommandHandler = command_handler.CommandHandler()
SPEECH : sr.SpeechRecognition = sr.SpeechRecognition(MANAGER)
SCREEN : s.Screen = s.Screen()

# CMDLINE

# DOESNT WORK IN SYSTEMCTL
# while True:
#     cmd = str(input("Command:\t")).split()
#     if(len(cmd) <= 0): continue
#     MANAGER.execute(cmd[0], *cmd[1:])
