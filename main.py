import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4
from PIL import Image,ImageDraw,ImageFont


# Initialize the display
epd = epd2in13_V4.EPD()
epd.init()
epd.Clear()

# Create a blank image
image = Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(image)

# Load font and draw text
font = ImageFont.load_default()
draw.text((10, 40), "Hello World", font=font, fill=0)

# Display the image
epd.display(epd.getbuffer(image))
epd.sleep()
