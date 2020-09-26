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
                "FuturePrcVol": future["FuturePrcVol"],
                "HedgePositionName": future["Name"],
                "OptimalHedgeRatio": round(hedge_ratio, 3),
                "NumFuturesContract": math.ceil(num_contracts)
            }
    result = {
        "outputs": [

        ]
    }
    for output in calculated.values():
        optimal_ratio = 1
        optimal_volatility = 99999999999999999
        sol_ratio = None
        sol_ratio = None
        sol = None
        for future in output.values():
            if future["OptimalHedgeRatio"] < optimal_ratio:
                optimal_ratio = future["OptimalHedgeRatio"]
                sol_ratio = future
            if future["FuturePrcVol"] < optimal_volatility:
                optimal_volatility = future["FuturePrcVol"]
                sol_volatility = future
        if sol_ratio != sol_volatility:
            if sol_ratio["NumFuturesContract"] < sol_volatility["NumFuturesContract"]:
                sol = sol_ratio
            else:
                sol = sol_volatility
        else:
            sol = sol_ratio
        sol.pop("FuturePrcVol", None)
        result["outputs"].append(sol)
            
            
    # result = calculated
    logging.info("My result :{}".format(result))
    return jsonify(result);



