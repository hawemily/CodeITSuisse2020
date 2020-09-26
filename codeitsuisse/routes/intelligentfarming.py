import logging
import json

from flask import request, jsonify

from codeitsuisse import app
import math

logger = logging.getLogger(__name__)


@app.route('/intelligent-farming', methods=['POST'])
def farming():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    seq = data.get("list")[0]["geneSequence"]
    seq = seq.lower()
    genes = {
        "a": seq.count("a"),
        "c": seq.count("c"),
        "g": seq.count("g"),
        "t": seq.count("t"),
    }
    sorted_seq = []
    logging.info("Start seq :{}".format(str(genes)))
    fillers_needed = math.ceil(genes["a"] / 2) - 1
    # always maximise cgt
    cgt = min([genes["c"], genes["g"], genes["t"]])
    genes["c"] -= cgt
    genes["g"] -= cgt
    genes["t"] -= cgt
    for i in range(cgt):
        sorted_seq.append("cgt")
    cc = math.floor(genes["c"]/2)
    excess_c = genes["c"] % 2
    for i in range(cc):
        sorted_seq.append("cc")
    if excess_c > 0:
        sorted_seq.append("c")
    for i in range(genes["g"]):
        sorted_seq.append("g")
    for i in range(genes["t"]):
        sorted_seq.append("t")
    index = 0
    while genes["a"] > 0:
        if genes["a"] >= 2:
            sorted_seq.insert(index, "aa")
            genes["a"] -= 2
            index += 2
        else:
            sorted_seq.insert(index, "a")
            genes["a"] -= 1
            index += 2
   
    logging.info("Sorted seq: {}".format(sorted_seq))
    sorted_string = "".join(sorted_seq).upper()
    result = data
    result["list"][0]["geneSequence"] = sorted_string
    logging.info("My result :{}".format(result))
    return jsonify(result)


# {
#     "runId": "a",
#     "list": [
#         {
#             "id": 1,
#             "geneSequence": "AAAAAACCTTTGGGGGGGTTTT"
#         }
#     ]
# }
