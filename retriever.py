import requests
import cv2
import numpy as np
from boundingbox import BoundingBox
from mapstyles import MapStyles


class Retriever:
    api_key = "pk.eyJ1IjoibWRpdHRnZW4iLCJhIjoiY2xlbjBiYjNmMHFkbTN1czBia3BiYzJ4NSJ9.OkLtkJ82TkrpkyzF4YmjeQ"

    def get_maptile(style, width, height, bbox):
        bbox_string = '[' + str(bbox.lowlong) + ',' + str(bbox.lowlat) + \
            ',' + str(bbox.uplong) + ',' + str(bbox.uplat) + ']'
        res_string = str(width) + 'x' + str(height) + '@2x'
        auth_string = "?access_token=" + Retriever.api_key
        resp = requests.get('https://api.mapbox.com/styles/v1/' + style.value +
                            '/static/' + bbox_string + '/' +
                            res_string + auth_string, stream=True).raw
        mapimage = np.asarray(bytearray(resp.read()), dtype="uint8")
        mapimage = cv2.imdecode(mapimage, cv2.IMREAD_COLOR)
        return mapimage
