from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2


class FrameMaker:

    # initialize a new frame with height and width in inches, and a MapStyle
    # enum style
    def __init__(self, width, height):
        self.width = (width * 300)
        self.height = (height * 300)
        self.frame = Image.new(mode="RGB", size=(
            self.width, self.height), color=(245, 245, 245))

    def addText(self, place, coordinates):
        palatino = ImageFont.truetype(
            'fonts/palatino.ttf', int(min(self.height, self.width) / 16))
        palatino_bold = ImageFont.truetype(
            'fonts/palatino-bold.ttf', (int(min(self.height, self.width) / 10)))
        tahoma = ImageFont.truetype(
            'fonts/tahoma.ttf', int(min(self.height, self.width) / 16))
        tahoma_bold = ImageFont.truetype(
            'fonts/tahoma-bold.ttf', (int(min(self.height, self.width) / 10)))

        T1 = ImageDraw.Draw(self.frame)
        T1.text((self.width / 25, self.height - (self.height / 5.0)),
                place, font=tahoma_bold, fill=(12, 12, 12))

        T2 = ImageDraw.Draw(self.frame)
        T2.text((self.width / 25, self.height - (self.height / 11.0)),
                coordinates, font=tahoma, fill=(12, 12, 12))

    # add opencv map im to frame

    def addImage(self, im):
        color_converted = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        combined = Image.fromarray(color_converted)
        self.frame.paste(
            combined, (int(self.width / 25), int(self.height / 25)))
