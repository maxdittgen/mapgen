import requests
import cv2
import numpy as np
from boundingbox import BoundingBox
import json
from mapstyles import MapStyles


class Retriever:
    api_key = "pk.eyJ1IjoibWRpdHRnZW4iLCJhIjoiY2xlbjBiYjNmMHFkbTN1czBia3BiYzJ4NSJ9.OkLtkJ82TkrpkyzF4YmjeQ"

    # given an enum MapStyle, float width and height resolution, and BoundingBox object of
    # coordinates, returns an opencv-readable image of the given tile
    def get_maptile(style, width, height, bbox):
        bbox_string = '[' + str(bbox.lowlong) + ',' + str(bbox.lowlat) + \
            ',' + str(bbox.uplong) + ',' + str(bbox.uplat) + ']'
        res_string = str(width) + 'x' + str(height + 80) + '@2x'
        auth_string = "?access_token=" + Retriever.api_key
        resp = requests.get('https://api.mapbox.com/styles/v1/' + style.value +
                            '/static/' + bbox_string + '/' +
                            res_string + auth_string, stream=True).raw
        mapimage = np.asarray(bytearray(resp.read()), dtype="uint8")
        mapimage = cv2.imdecode(mapimage, cv2.IMREAD_COLOR)
        cropped = mapimage[0:(mapimage.shape[0] - 80), 0:mapimage.shape[1]]
        return cropped

    # returns list of coordinates [long, lat] of search string location
    def get_coords(searchloc):
        search = searchloc.replace(" ", "%20")
        resp = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/" +
                            search + ".json?access_token=" +
                            Retriever.api_key)
        data = resp.json()

        # edit this to get full list of possibilities later on
        return ((data['features'])[0])['center']

    # Requires:
    # - searchloc: a search string representing a location of center of map
    # - width: float representing number of miles the image is wide
    # - aspect: float representing width divided by height of desired map
    # Returns: Bounding box object
    def get_bounding_box(loc_coords, width, aspect):
        heightlat = (width / aspect) / 69.0
        widthlong = width / 54.6
        return BoundingBox(loc_coords[0] - (widthlong / 2),
                           loc_coords[1] - (heightlat / 2),
                           loc_coords[0] + (widthlong / 2),
                           loc_coords[1] + (heightlat / 2))
