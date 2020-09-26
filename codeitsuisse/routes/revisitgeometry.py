import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        result = a[0] * b[1] - a[1] * b[0]
        return result

    div = det(xdiff, ydiff)
    if div == 0:
        return
        
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    # check bounds
    min_x = min(line1[0][0], line1[1][0])
    max_x = max(line1[0][0], line1[1][0])
    min_y = min(line1[0][1], line1[1][1])
    max_y = max(line1[0][1], line1[1][1])
    if (min_x <= x <= max_x and min_y <= y <= max_y) :
        return round(x, 2), round(y, 2)
    else:
        return None, None

@app.route('/revisitgeometry', methods=['POST'])
def geometry():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")
    solutions = []
    for i in range(len(shapeCoordinates) - 1):
        x, y = line_intersection(
            [[shapeCoordinates[i]["x"], shapeCoordinates[i]["y"]], # start point
            [shapeCoordinates[i+1]["x"], shapeCoordinates[i+1]["y"]]] # end point
            ,
            [[lineCoordinates[0]["x"], lineCoordinates[0]["y"]],  # start point
            [lineCoordinates[1]["x"], lineCoordinates[1]["y"]]])
        if x != None and y != None:
            logging.info("Intersection found between line and edge {}".format(i))
            solutions.append({"x": x, "y": y})
    
    i = len(shapeCoordinates) - 1
    x, y = line_intersection(
        [[shapeCoordinates[i]["x"], shapeCoordinates[i]["y"]], # start point
        [shapeCoordinates[0]["x"], shapeCoordinates[0]["y"]]] # end point
        ,
        [[lineCoordinates[0]["x"], lineCoordinates[0]["y"]],  # start point
        [lineCoordinates[1]["x"], lineCoordinates[1]["y"]]])
    if x != None and y != None:
        logging.info("Intersection found between line and edge {}".format(i))
        solutions.append({"x": x, "y": y}) 

    logging.info("My result :{}".format(solutions))
    return json.dumps(solutions)
