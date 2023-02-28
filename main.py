import cv2
from retriever import Retriever
from mapstyles import MapStyles
from boundingbox import BoundingBox
from framemaker import FrameMaker

# given a mapstyle enum, place search string, diameter (in miles), and width and
# height in inches, generates a 300ppi png of the place


def make_poster(style, place, diameter, width, height):
    frame = FrameMaker(width, height)
    im = Retriever.get_map(style, place, diameter,
                           width * 23.0 / 50, height * 7.0 / 20.0)
    coords = Retriever.get_coords_string(place)
    frame.addText(place, coords)
    frame.addImage(im)
    frame.frame.show()


make_poster(MapStyles.BLUEPRINT, "Cornell University, NY", 2, 17, 12)


# im = Retriever.get_map(MapStyles.BLUEPRINT, "Pittsburgh, PA", 5, 9.2, 7)
# cv2.imshow('map', im)
# cv2.waitKey(0)

# f1 = FrameMaker(10, 10)
# f1.addText("New York", "a set of coordinates")

# Retriever.get_map(MapStyles.BLUEPRINT, "515 E 89th St", 5, 4, 5)

# im = Retriever.get_map_test(MapStyles.BLUEPRINT, "515 E 89th St", 5, 720, 480)
# cv2.imshow('map', im)
# cv2.waitKey(0)

# im = Retriever.get_maptile(MapStyles.SATELLITE, 1240, 1240,
#                            Retriever.get_bounding_box("515 E 89th St, New York", 0.5, 0.5))
# cv2.imshow('map', im)
# cv2.waitKey(0)
