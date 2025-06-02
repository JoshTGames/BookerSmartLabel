import command_handler
MANAGER : command_handler.CommandHandler = command_handler.CommandHandler()


while True:
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
#                 screen.display_text([[result["text"], "h3"]], 10)
#                 print("You said:", result["text"])
#             # name = str(input("Text:\t"))
#             # role = str(input("Role:\t"))
#             # screen.display_text([[input("Text:\t"), "h1"], [input("Role:\t"), "h3"], [input("Role:\t"), "h3"]], 10)

# except KeyboardInterrupt:
#     screen.epd2in13_V4.epdconfig.module_exit(cleanup=True)
#     exit()

# # try:


# #     # Initialize the display
# #     epd = epd2in13_V4.EPD()
# #     epd.init_fast()
# #     epd.Clear()
# #     # font = ImageFont.load_default()
# #     font = ImageFont.truetype("p/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)

# #     debugText = "Hello Booker! >:D\nI am the smart tag"

# #     # Create a blank image
# #     image = Image.new('1', (epd.heig ht, epd.width), 255)
# #     draw = ImageDraw.Draw(image)

# #     bbox = draw.textbbox((0,0), debugText, font=font)
# #     h, w = bbox[2] - bbox[0], bbox[3] - bbox[1]

# #     x = (epd.width - w) // 2
# #     y = (epd.height - h) // 2


# #     # Load font and draw text    
# #     draw.text((y, x), debugText, font=font, fill=0)

# #     # Display the image
# #     epd.display_fast(epd.getbuffer(image))
# #     epd.sleep()
# # except KeyboardInterrupt:
# #     epd2in13_V4.epdconfig.module_exit(cleanup=True)
# #     exit()
