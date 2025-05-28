import epd2in13_V3  # Adjust for your display version
from PIL import Image, ImageDraw, ImageFont

# Initialize the display
epd = epd2in13_V3.EPD()
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
