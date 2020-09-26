import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def match(a, b):
    if a.lower() == b.lower():
        return True
    else:
        return False

@app.route('/inventory-management', methods=['POST'])
def search():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    query = data.get("searchItemName")
    items = data.get("items")
    for item in items:
        index = 0
        while index < len(query):
            if match(query[index], item[index]):
                index += 1
            elif match(query[index], item[index + 1]):
                # insert item
                pass
            elif match(query[index + 1], item[index]):
                # delete item 
                pass
            else:
                # swap letters
                pass

    result = None
    logging.info("My result :{}".format(result))
    return json.dumps(result)
