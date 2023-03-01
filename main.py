# imports
from flask import Flask, render_template, request, redirect, url_for, session
from retriever import Retriever
from mapstyles import MapStyles
from framemaker import FrameMaker

# init flask
app = Flask(__name__)

# secret key
app.config["SECRET_KEY"] = 'cb72c9bbe674d6d8488b0d5a383c81a3'

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


# make_poster(MapStyles.BLUEPRINT, "Manhattan, NY", 10, 10, 12)

# routing

# routing to main page


@app.route("/", methods=['GET', 'POST'])
def main():
    # define session defaults:
    if (session == {}):
        session["width"] = 10
        session["height"] = 8
        session["place"] = "New York, NY"
        session["diameter"] = 5
        session["coordinates"] = Retriever.get_coords(session["place"])
        session["style"] = "WHITE"

    return render_template('index.html')


# routing to map creation page
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # submission button was pressed
        session["width"] = int(request.form.get("width"))
        session["height"] = int(request.form.get("height"))
        return render_template('create.html', message=(str(session["width"]) + " inches wide by " + str(session["height"]) + " inches tall selected"))

    return render_template('create.html', message="")
