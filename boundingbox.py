class BoundingBox:
    def __init__(self, lowlong, lowlat, uplong, uplat):
        self.lowlong = lowlong
        self.lowlat = lowlat
        self.uplong = uplong
        self.uplat = uplat

    def __str__(self):
        return ("[(" + str(self.lowlat) + ", " + str(self.lowlong) +
                ") , (" + str(self.uplat) + ", " + str(self.uplong) + ")]")
