import sys, os, time

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from lib import screen, json
settings = json.ReadFile(os.getcwd() + '/settings.json')
font = settings['default-font']


try:
    while True:
        screen.clear()
        name = str(input("Text:\t"))
        screen.display_text([[name, 1, font]])
except KeyboardInterrupt:
    screen.epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()

# try:


#     # Initialize the display
#     epd = epd2in13_V4.EPD()
#     epd.init_fast()
#     epd.Clear()
#     # font = ImageFont.load_default()
#     font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)

#     debugText = "Hello Booker! >:D\nI am the smart tag"

#     # Create a blank image
#     image = Image.new('1', (epd.height, epd.width), 255)
#     draw = ImageDraw.Draw(image)

#     bbox = draw.textbbox((0,0), debugText, font=font)
#     h, w = bbox[2] - bbox[0], bbox[3] - bbox[1]

#     x = (epd.width - w) // 2
#     y = (epd.height - h) // 2


#     # Load font and draw text    
#     draw.text((y, x), debugText, font=font, fill=0)

#     # Display the image
#     epd.display_fast(epd.getbuffer(image))
#     epd.sleep()
# except KeyboardInterrupt:
#     epd2in13_V4.epdconfig.module_exit(cleanup=True)
#     exit()
