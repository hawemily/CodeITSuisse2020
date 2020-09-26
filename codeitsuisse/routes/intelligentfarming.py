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
    # always maximise cgt as long as it does not produce aaa sequences
    cgt = min([genes["c"], genes["g"], genes["t"]])
    genes["c"] -= cgt
    genes["g"] -= cgt
    genes["t"] -= cgt
    num_fillers = genes["c"] + genes["g"] + genes["t"] + cgt
    logging.info("fillers present: {}".format(num_fillers))
    fillers_needed = math.ceil(genes["a"]/2) - 1
    logging.info("fillers needed: {}".format(fillers_needed))
    excess_fillers = num_fillers - fillers_needed
    logging.info("excess fillers: {}".format(excess_fillers))
    if excess_fillers <= 0:
        excess = math.ceil(abs(excess_fillers)/2)
        excess = min([excess, cgt])
        logging.info("excess cgt: {}".format(excess))
        cgt -= excess
        genes["c"] += excess
        genes["g"] += excess
        genes["t"] += excess
    for i in range(cgt):
        sorted_seq.append("cgt")
    # maximise cc sequences next
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
