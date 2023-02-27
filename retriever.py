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

    # given a style, location search string, map width (miles), and
    # height and width in inches, returns a properly scaled 300ppi print image
    def get_map(style, searchloc, radius, width, height):
        pixel_width = width * 300
        pixel_height = height * 300
        center_coords = Retriever.get_coords(searchloc)
        bbox = Retriever.get_bounding_box(center_coords, radius, width/height)

        # create matrix of width and height of each 1000x1000 image
        dims = [[]]
        i = pixel_width
        j = pixel_height
        while i > 0:
            dims[0].append([min(i, 1000), 0])
            i = i - (min(i, 1000))
        while j > 0:
            temp_height = min(j, 1000)
            dim = []
            for i in range(len(dims[-1])):
                dim.append([dims[-1][i][0], temp_height])
            j = j - temp_height
            dims.append(dim)
        dims = dims[1:]

        # create matrix of bounding box of each 1000x1000 matrix in bounding box
        lats = []
        longs = []
        distance_moved = 0
        total_lat = bbox.uplat - bbox.lowlat
        total_long = bbox.uplong - bbox.lowlong
        for i in range(len(dims)):
            uplat = bbox.uplat - (distance_moved)
            botlat = bbox.uplat - \
                (distance_moved + ((dims[i][0][1] / pixel_height) * total_lat))
            lats.append((botlat, uplat))
            distance_moved = distance_moved + \
                ((dims[i][0][1] / pixel_height) * total_lat)
        distance_moved = 0
        for i in range(len(dims[0])):
            leftlong = bbox.lowlong + (distance_moved)
            rightlong = bbox.lowlong + \
                (distance_moved + ((dims[0][i][0] / pixel_width) * total_long))
            longs.append((leftlong, rightlong))
            distance_moved = distance_moved + \
                ((dims[0][i][0] / pixel_width) * total_long)
        bboxes = [[BoundingBox(0, 0, 0, 0) for i in range(len(longs))] for j
                  in range(len(lats))]
        for i in range(len(lats)):
            for j in range(len(longs)):
                bboxes[i][j] = BoundingBox(
                    longs[j][0], lats[i][0], longs[j][1], lats[i][1])

        print(str(bboxes[0][0]) + str(dims[0][0]) +
              "\n" + str(bboxes[0][1]) + str(dims[0][1]) +
              "\n" + str(bboxes[1][0]) + str(dims[1][0]) +
              "\n" + str(bboxes[1][1]) + str(dims[1][1]))

        # create matrix of map_tiles
        tiles = [[np.empty(0) for i in range(len(longs))] for j
                 in range(len(lats))]
        for i in range(len(lats)):
            for j in range(len(longs)):
                tiles[i][j] = Retriever.get_maptile(
                    style, dims[i][j][0], dims[i][j][1], bboxes[i][j])

        # concatenate images together
        bars = []
        for i in range(len(lats)):
            bars.append(np.concatenate(tiles[i], axis=1))
        return np.concatenate(bars)
