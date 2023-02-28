# imports
from flask import Flask, render_template, request, redirect, url_for, session
from retriever import Retriever
from mapstyles import MapStyles
from framemaker import FrameMaker

# init flask
app = Flask(__name__)

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


# make_poster(MapStyles.BLUEPRINT, "Cornell University, NY", 2, 4, 3)

# routing

# routing to main page


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')
