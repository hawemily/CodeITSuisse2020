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
    # always maximise cc
    excess_c = genes["c"] % 2
    num_fillers = genes["g"] + genes["t"] + excess_c
    excess_fillers = fillers_needed - num_fillers
    if excess_fillers >= 2 and excess_c == 1:
        # form one ACGT 
        sorted_seq.append("acgt")
        genes["g"] -= 1
        genes["t"] -= 1
        genes["a"] -= 1
        genes["c"] -= 1
        for i in range(math.floor(genes["c"]/2)):
            sorted_seq.append("cc")
        for i in range(genes["g"]):
            sorted_seq.append("g")
        for i in range(genes["t"]):
            sorted_seq.append("t")
        sorted_seq.insert(0, "a")
        index = 1
        while genes["a"] > 0:
            if genes["a"] >= 2:
                sorted_seq.insert(index, "aa")
                genes["a"] -= 2
                index += 2
            else:
                sorted_seq.insert(index, "a")
                genes["a"] -= 1
                index += 2

    elif excess_fillers >= 0:
        # form no ACGT
        for i in range(math.floor(genes["c"]/2)):
            sorted_seq.append("cc")
        if excess_c > 0:
            sorted_seq.append("c")
        for i in range(genes["g"]):
            sorted_seq.append("g")
        for i in range(genes["t"]):
            sorted_seq.append("t")
        l = len(sorted_seq)
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
    else: 
        # lump all excess As together
        # form no ACGT
        for i in range(math.floor(genes["c"]/2)):
            sorted_seq.append("cc")
        if excess_c > 0:
            sorted_seq.append("c")
        for i in range(genes["g"]):
            sorted_seq.append("g")
        for i in range(genes["t"]):
            sorted_seq.append("t")
        l = len(sorted_seq)
        index = 0
        while genes["a"] > 0 and index < len(sorted_seq):
            if genes["a"] >= 2:
                sorted_seq.insert(index, "aa")
                genes["a"] -= 2
                index += 2
            else:
                sorted_seq.insert(index, "a")
                genes["a"] -= 1
                index += 2
        for i in range(genes["a"]):
            sorted_seq.append("a") # lump excess As at the end
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
