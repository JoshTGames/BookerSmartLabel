import sys, os, logging
from typing import List, Tuple

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont

from lib import json
fontSettings = json.ReadFile(os.getcwd() + '/settings.json')['text']

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




def display_text(textData: List[Tuple[str, str]]):
    """
    Distributes text on the 2"13V4 waveshare screen

    Parameters:
    textData (array): [[string, string],...] - text, fontStyle
    """
    image = Image.new('1', (HEIGHT, WIDTH), 255)
    draw = ImageDraw.Draw(image)

    height = 0
    
    for txt, sizing in textData:
        font = ImageFont.truetype(fontSettings['font'], fontSettings['sizing'][sizing])
        bbox = font.getbbox(txt)
        
        tH = (bbox[3] - bbox[1])

        draw.text((HEIGHT//2, ((WIDTH//2) * 0) + (height + tH / 2)), txt, font=font, fill=0, anchor="mm", align="center")
        height += tH

    clear()
    epd.display_fast(epd.getbuffer(image))


def sleep() -> None:
    logging.info(epdName + " sleeping...")
    epd.sleep()

def clear() -> None:
    logging.info(epdName + " clearing...")
