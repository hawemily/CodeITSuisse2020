import logging
import json
import sys

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def checkAndMarkSurroundingGrids(minI, maxI, minJ, maxJ, data, i, j):
    if data[i][j] == '*':
        return

    for m in range(minI, maxI + 1):
        for n in range(minJ, maxJ + 1):

            if int(data[i][j]) > 0 and data[m][n] == '0':
                data[m][n] = '1'


def checkForSurroundingOnes(startI, endI, endJ, startJ, i, j, data, maxCount):
    if not data[i][j].isnumeric():
        return maxCount

    currMin = sys.maxsize
    logging.info("i: " + str(i) + " " + "j: " + str(j))
    for m in range(startI, endI + 1):
        for n in range(startJ, endJ + 1):
            if (m >= i and n >= j) or m > i:
                break
            logging.info("m1 " + str(m) + " n1: " + str(n))
            if data[m][n].isnumeric():
                logging.info("m: " + str(m) + " n: " + str(n))
                currMin = min(currMin, int(data[m][n]))

    logging.info("currMin: " + str(currMin))
    if currMin != sys.maxsize:
        data[i][j] = str(currMin)

    if currMin == sys.maxsize and int(data[i][j]) > 0:
        logging.info("changing to maxCount " + str(i) + " " + str(j))
        data[i][j] = str(maxCount)
        maxCount = maxCount + 1


    if data[startI][endJ].isnumeric() and int(data[startI][endJ]) > currMin:
        data[startI][endJ] = str(currMin)
    logging.info("after every round: " + str(data))
    return maxCount


def countNoOfClusters(data):
    n = len(data)
    for i in range(n):
        m = len(data[i])
        for j in range(m):
            startI = i if (i - 1 < 0) else i - 1
            endI = i if (i + 1 >= n) else i + 1
            startJ = j if (j - 1 < 0) else j - 1
            endJ = j if (j + 1 >= m) else j + 1
            checkAndMarkSurroundingGrids(startI, endI, startJ, endJ, data, i, j)
    logger.info(data)
    logger.info(type(data[0][0]))

    maxCount = 2
    if data[0][0] == '1':
        data[0][0] = str(maxCount)
    logger.info("second data before: " + str(data))
    for i in range(n):
        m = len(data[i])
        for j in range(m):
            if i == 0 and j == 0:
                continue
            if i == 0 and j >= 1:
                if data[i][j] == '1':
                    if data[i][j - 1].isnumeric():
                        data[i][j] = data[i][j - 1]
                    else:
                        maxCount += 1
                        data[i][j] = str(maxCount)
            else:
                startJ = j if (j - 1 < 0) else j - 1
                endJ = j if (j + 1 >= m) else j + 1
                startI = i if (i - 1 < 0) else i - 1
                endI = i if (i + 1 >= n) else i + 1
                maxCount = checkForSurroundingOnes(startI, endI, endJ, startJ, i, j, data, maxCount)

    logger.info("second iteration data" + str(data))
    bitmap = {}
    numberOfClusters = 0
    for i in range(n):
        m = len(data[i])
        for j in range(m):
            if data[i][j].isnumeric() and data[i][j] not in bitmap.keys() and int(data[i][j]) != 0:
                numberOfClusters += 1
                bitmap[data[i][j]] = True

    return numberOfClusters





@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    logging.info(type(data))
    result = countNoOfClusters(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
