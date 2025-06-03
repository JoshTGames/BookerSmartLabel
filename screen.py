import threading, sys, os
from queue import Queue as q
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import json_manager as j

from waveshare_epd import epd2in13_V4
from PIL import Image, ImageDraw, ImageFont

from typing import List, Tuple

class Text:
    """Used to manipulate text more appropriately for EPD screens"""

    instance = None

    def __get_size(font, text):
        """Calculates width/height of parsed text
            Args:
                font (ImageFont): The font we are wanting to use
                text (str): The text we are querying

            Returns:
                width, height (Tuple(int, int)): width & height of screen
        """
        bbox = font.getbbox(text)
        return bbox[2] - bbox[1], bbox[3] - bbox[0]

    def __init__(self, font_settings):
        self.font_path = font_settings['font']
        self.sizing_sheet = font_settings['sizing']
        self.min_size = font_settings['min-size']
        self.anchor_interface = {
            "center": "mm",
            "left": "lm",
            "right": "rm"
        }        
        Text.instance = self

    def create_wrapper(self, size: Tuple[int, int], spacing: int, *text: Tuple[str, str, str]) -> Image:
        """Creates a wrapper to design the text image to be displayed onto the screen
            Args:
                size (Tuple[int, int]): width/height of wrapper
                spacing (int): space between each line
                *text (Tuple[str, str, str]): Text, font size (h1/h2/h3...), Alignment (center/left/right)
            
            Returns:
                Image: Visual to be presented onto the screen
        """
        
        # For some reason, it seems waveshare flips Width/Height around. I am having to correct this in code
        WIDTH: int = size[1]
        HEIGHT: int = size[0]
        image = Image.new("1", (WIDTH, HEIGHT), 255)
        draw = ImageDraw.Draw(image)

        heights: List[Tuple[ImageFont, str, str, int]] = [] # Font, txt, alignment, height
        total_height = 0

        # Process text to reduce fontsize & wrap on a new line if needed
        for t, s, a in text:                    
            desired_size: int = self.sizing_sheet[s]
            font: ImageFont = ImageFont.truetype(self.font_path, desired_size)
            font = self.__adjust_for_width(font, desired_size, WIDTH, t)
            
            _, h = Text.__get_size(font, t)
            lines = self.__wrap_text(font, WIDTH, t)
            for l in lines:
                heights.append((font, l, a, h))
                total_height += h                

        # Calculate spacing
        total_spacing = spacing * (len(heights) - 1) if len(heights) > 1 else 0
        content_height = total_height + total_spacing

        # Pointers for managing height
        y_start = (HEIGHT - content_height) // 2
        y_cursor = y_start

        # Converts desired alignment to a positioning on the screen 
        x_pos = {
            "center": WIDTH//2,
            "left": 0,
            "right": WIDTH
        }      

        for f, t, a, h in heights:            
            draw.text((x_pos[a], y_cursor + h // 2), t, font=f, fill=0, anchor=self.anchor_interface[a], align=a)
            y_cursor += h + spacing
        return image
        
    def __adjust_for_width(self, font: ImageFont, desired_font_size: int, max_width: int, *text: str) -> ImageFont:
        """Calculates a size for the text so it will all fit within the width of the screen
            Args:
                font (ImageFont): The font we are using
                desired_font_size (int): The desired font size we are wanting
                max_width (int): The max width the text is allowed to fit within
                *text (List(str)): A list of text we are wanting to account for
        """
        final_size = desired_font_size
        for x in text:
            x_size = desired_font_size

            width, _ = Text.__get_size(font, x)
            while width > max_width and x_size > self.min_size:
                x_size -= 1
                width, _ = Text.__get_size(ImageFont.truetype(self.font_path, x_size), x)
            
            # If x_size is less than size, apply
            final_size = x_size if x_size < final_size else final_size 
        return ImageFont.truetype(self.font_path, final_size)

    def __wrap_text(self, font: ImageFont, max_width: int, text: str):
        """If text exceeds the max width, it'll be spread out across multiple lines
            Args:
                font (ImageFont): the font being used
                max_width (int): max width till a new line is required
                text (str): the text we are writing to the screen
        """
        words = text.split(" ")
        lines = []
        cur_line = ""

        for word in words:
            tst_line = f'{cur_line} {word}'.strip()
            width, _ = Text.__get_size(font, tst_line)
            if(width > max_width):
                lines.append(cur_line)
                cur_line = word
                continue
            cur_line = tst_line
        
        if cur_line:
            lines.append(cur_line)
        return lines


class Screen:
    """Class to manage our screen"""

    display_lock = threading.Lock()
    instance = None

    def __init__(self, do_log: bool = False):
        """Constructor for our screen"""
        self.EPD = epd2in13_V4.EPD()
        self.EPD_VERSION = "EPD2\"13V4"
        self.WIDTH, self.HEIGHT = self.EPD.width, self.EPD.height
        self.running = True
        self.sleeping = False
        self.display_queue: q[Image] = q()
        
        self.do_log = do_log

        settings = j.read_file(os.getcwd() + '/settings.json')['text']

        self.TEXT = Text(settings)

        try:
            self.init(False, True)
            self.__log("Display Active!")
        except IOError as e:
            self.__log(f"Display Failed!\n{e}")
            return

        self.thread = threading.Thread(target=self.__display_async, daemon=True)
        self.thread.start()

        Screen.instance = self

    def __display_async(self):
        """Runs asyncronously on a thread"""
        while self.running:
            image = self.display_queue.get(block=True)
            if(self.sleeping):
                self.init(False, True)

            with Screen.display_lock:
                self.clear()
                self.EPD.display(self.EPD.getbuffer(image))
                if(self.display_queue.empty()):
                    self.sleep()

    def set_text(self, spacing: int = 10, *text: Tuple[str, str, str]) -> None:
        """Presents a visual to the screen - Adds image to queue to be presented
            Args:
                spacing (int): space between each line
                *text (Tuple[str, str, str]): Text, font size (h1/h2/h3...), Alignment (center/left/right)
        """
        self.display_queue.put(self.TEXT.create_wrapper((self.WIDTH, self.HEIGHT), spacing, *text))

    #--- Helpful methods
    def __log(self, msg: str): 
        """Logs to console
        Args:
            msg (str): Message to output to console
        """
        if(not self.do_log): return
        print(f"{self.EPD_VERSION}: {msg}")

    def init(self, fast: bool = False, clean: bool = False) -> None:
        """Awakes the screen -- Not threaded on its own
        Args:
            fast (bool): Do we want a soft/hard initialisation?
            clean (bool): Do we want to clean the screen after initialisation?
        """

        _ = self.EPD.init_fast() if fast else self.EPD.init() # Conditional init based on if we want it fast or not
        self.sleeping = False
        if(clean):
            self.clear()

    def clear(self) -> None:
        """Clears the screen -- Not threaded on its own"""
        self.__log("Clearing...")
        self.EPD.Clear()

    def sleep(self) -> None:
        """Puts screen in power saving mode -- Not threaded on its own"""
        self.__log("Sleeping...")
        self.EPD.sleep()
        self.sleeping = True