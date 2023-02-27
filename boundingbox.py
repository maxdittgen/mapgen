class BoundingBox:
    def __init__(self, ur, ul, lr, ll):
        self.upright = ur
        self.upleft = ul
        self.lowright = lr
        self.lowleft = ll