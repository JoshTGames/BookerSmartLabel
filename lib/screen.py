import sys, os, logging
from typing import List, Tuple

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont

epd = None
epdName = "epd2\"13V4"
try:
    # Initialize the display
    epd = epd2in13_V4.EPD()
    epd.init_fast()
    epd.Clear()
    logging.info(epdName + " active!")
except IOError as e:
    logging.info(epdName + " failed... \n" + e)

# SCREEN CONSTS
WIDTH, HEIGHT = epd.width, epd.height




def display_text(textData: List[Tuple[str, float]], fontType):
    """
    Distributes text on the 2"13V4 waveshare screen

    Parameters:
    textData (array): [[string, float, string],...] - text, scale between 0-1, fontType
    padding (float): Distance away from screen border
    spacing (float): Distance away from other elements
    """
    image = Image.new('1', (HEIGHT, WIDTH), 255)
    draw = ImageDraw.Draw(image)
    
    txtScale = sum([item[1] for item in textData])

    for t, s in textData:
        font = ImageFont.truetype(fontType, 24)
        bbox = font.getbbox(t)

        tWidth = bbox[2] - bbox[0]

        # h: int = (s / txtScale) * HEIGHT #
        h =0
        w: int = (WIDTH - tWidth) // 2 # Centers on X-axis

        draw.text((w,h), t, font=font, fill=0, anchor="mm", align="center")




    # yStart = 0
    # y = yStart
    
    # for txt, scl in textData:        
        # maxH = int((scl / txtScale) * HEIGHT) # Scales the text proportionately to the screen height
        # maxW = int(WIDTH / len(txt))
        # size = min(maxH, maxW)
        
        # font = ImageFont.truetype(fontType, size)

        # bbox = draw.textbbox((0, 0), txt, font=font)

        # y += bbox[3] - bbox[1] # Get text height
        # x = (WIDTH - (bbox[2] - bbox[0])) // 2 # Center horizontal

        # draw.text((x, y), txt, font=font, fill=0)

    clear()
    epd.display_fast(epd.getbuffer(image))


def sleep() -> None:
    logging.info(epdName + " sleeping...")
    epd.sleep()

def clear() -> None:
    logging.info(epdName + " clearing...")
