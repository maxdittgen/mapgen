from PIL import Image
from mapstyles import MapStyles


class FrameMaker:

    # initialize a new frame with height and width in pixels, and a MapStyle
    # enum style
    def __init__(self, width, height, style):
        self.width = width
        self.height = height
        self.frame = Image.new(mode="RGB", size=(
            width, height), color=(252, 247, 237))
