from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class FrameMaker:

    # initialize a new frame with height and width in inches, and a MapStyle
    # enum style
    def __init__(self, width, height):
        self.width = width * 300
        self.height = height * 300
        self.frame = Image.new(mode="RGB", size=(
            width, height), color=(252, 247, 237))

    def addText(self, place, coordinates):
        palatino = ImageFont.truetype(
            'fonts/palatino.ttf', int(self.height / 11))
        palatino_bold = ImageFont.truetype(
            'fonts/palatino-bold.ttf', int(self.height / 8))

        T1 = ImageDraw.Draw(self.frame)
        T1.text((self.width / 25, self.height - (self.height / 5.0)),
                place, font=palatino_bold, fill=(2, 25, 111))

        T2 = ImageDraw.Draw(self.frame)
        T2.text((self.width / 25, self.height - (self.height / 10.0)),
                coordinates, font=palatino, fill=(2, 25, 111))

        self.frame.show()
