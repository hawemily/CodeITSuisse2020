import logging
import json
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def search():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for item in data:
        query = item.get("searchItemName")
        items = item.get("items")
        dictionary = {}
        items.sort(key=(lambda x: distanceFromQueryStr(x, query, dictionary)))

        newitems = []
        if len(items) > 10:
            newitems = items[:10]
        else:
            newitems = items

        newitems = str(list(map(lambda x: dictionary.get(x), newitems)))
        logging.info(newitems)
        logging.info("My ehnlo :{}".format(newitems))
        result.append({"searchItemName": query, "searchResult": newitems})

    logging.info("My result :{}".format(result))
    return json.dumps(result)


def minOperation(addLen, delLen, subLen):
    minlen = min(addLen, delLen, subLen)

    for (k, v) in ((0, addLen), (1, delLen), (2, subLen)):
        if v == minlen:
            return k, v
    return -1, -1


def distanceFromQueryStr(itemString, queryString, dictionary):
    sizeItem = len(itemString) + 1
    sizeQuery = len(queryString) + 1
    matrix = [[0 for x in range(sizeQuery)] for x in range(sizeItem)]

    matrix[0][0] = (0, "")
    for i in range(1, sizeItem):
        matrix[i][0] = (i, "+" + itemString[i - 1])
    for j in range(1, sizeQuery):
        matrix[0][j] = (j, "-" + queryString[j - 1])

    for i in range(1, sizeItem):
        for j in range(1, sizeQuery):
            (addLen, additionOfOutput) = matrix[i - 1][j]
            (delLen, deletionOfInput) = matrix[i][j - 1]
            (substLen, substitution) = matrix[i - 1][j - 1]
            k, v = -1, -1
            if itemString[i - 1] == queryString[j - 1]:
                k, v = minOperation(addLen + 1, delLen + 1, substLen)
            else:
                k, v = minOperation(addLen + 1, delLen + 1, substLen + 1)

            if k == 0:
                matrix[i][j] = (v, additionOfOutput + "+" + itemString[i - 1])
            elif k == 1:
                matrix[i][j] = (v, deletionOfInput + "-" + queryString[j - 1])
            else:
                matrix[i][j] = (v, substitution + itemString[i - 1])

    minEditDistance, editStringReconstructed = matrix[sizeItem - 1][sizeQuery - 1]
    dictionary[itemString] = editStringReconstructed
    return minEditDistance


