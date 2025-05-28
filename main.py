import sys
import os

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4
from PIL import Image,ImageDraw,ImageFont
import logging

logging.basicConfig(level=logging.DEBUG)
logging.info("Booker smart label V0.01-PREALPHA")

try:
    logging.info("Booker smart label V0.01-PREALPHA")

    # Initialize the display
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear()
    font = ImageFont.load_default()

    debugText = "Hello World!"

    # Create a blank image
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0,0), debugText, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x, y = (epd.width - w) // 2, (epd.height - h) //2

    # Load font and draw text    
    draw.text((x, y), debugText, font=font, fill=0)

    # Display the image
    epd.display(epd.getbuffer(image))
    epd.sleep()
except KeyboardInterrupt:
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
