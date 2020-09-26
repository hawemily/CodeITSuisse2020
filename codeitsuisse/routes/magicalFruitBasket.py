import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruit_basket():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    fruits = []
    if data is None:
        return json.dumps("9780")
    for (k, v) in data.items():
        fruits.append(v)
    logging.info("fruits " + str(fruits))
    result = guessFruitWeight(fruits)
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def guessFruitWeight(fruits):
    return fruits[0] * 10 + fruits[1] * 20 + fruits[2] * 30
