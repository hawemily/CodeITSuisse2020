import logging
import json
import sys

from flask import request, jsonify;
from decimal import Decimal

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_portfolio():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputs = data["inputs"]

    ls = []
    for input in inputs:
        portfolio = input["Portfolio"]
        (lowestFutName, lowestHR, lowestFutures) = calculateLowestHedge(input["IndexFutures"], portfolio["Value"],
                                                                        portfolio["SpotPrcVol"])
        ls.append(
            {"HedgePositionName": lowestFutName, "OptimalHedgeRatio": lowestHR, "NumFuturesContract": lowestFutures})

    outputs = {"outputs": ls}

    logging.info("My result :{}".format(outputs))
    return json.dumps(outputs, cls=DecimalEncoder)


def calculateLowestHedge(indexFutures, value, spotPrcSD):
    lowestFutures = sys.maxsize
    lowestHR = 0
    lowestFut = ""
    for indexFuture in indexFutures:
        hedgeRatio = Decimal(str(indexFuture["CoRelationCoefficient"] * spotPrcSD / indexFuture["FuturePrcVol"]))
        roundedHedgeRatio = round(hedgeRatio, 3)
        logger.info("rounderhedgeratio typee: " + str(type(roundedHedgeRatio)))
        futuresContract = Decimal(
            str(roundedHedgeRatio * value / Decimal(str((indexFuture["IndexFuturePrice"] * indexFuture["Notional"])))))
        roundFutureContract = int(round(futuresContract))
        if lowestFutures > roundFutureContract:
            lowestFutures = roundFutureContract
            lowestHR = roundedHedgeRatio
            lowestFut = indexFuture["Name"]
    return lowestFut, lowestHR, lowestFutures


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
