import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import math

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])

def portfolio():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs");
    calculated = {}
    for input in inputs:
        portfolio = input["Portfolio"]
        calculated[portfolio["Name"]] = {}
        futures = input["IndexFutures"]
        for future in futures:
            hedge_ratio = future["CoRelationCoefficient"] * \
                portfolio["SpotPrcVol"] / future["FuturePrcVol"]
            contract_size = future["IndexFuturePrice"] * future["Notional"]
            num_contracts = hedge_ratio * portfolio["Value"] / contract_size
            calculated[portfolio["Name"]][future["Name"]] = {
                "HedgePositionName": future["Name"],
                "OptimalHedgeRatio": round(hedge_ratio, 3),
                "NumFuturesContract": math.ceil(num_contracts)
            }
    result = {
        "outputs": [

        ]
    }
    for output in calculated.values():
        optimal = 1
        sol = None
        for future in output.values():
            if future["OptimalHedgeRatio"] < optimal:
                optimal = future["OptimalHedgeRatio"]
                sol = future
        result["outputs"].append(sol)
            
            
    # result = calculated
    logging.info("My result :{}".format(result))
    return jsonify(result);



