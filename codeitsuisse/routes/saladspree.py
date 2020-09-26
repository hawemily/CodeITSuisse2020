import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def saladspree():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    num_salads = data.get("number_of_salads");
    street_map = data.get("salad_prices_street_map");
    spent = 0
    for street in street_map:
        consecutives = []
        consecutive = []
        for store in street:
            if store == 'X':
                consecutives.append(consecutive)
                consecutive = []
            else: 
                consecutive.append(int(store))
        consecutives.append(consecutive)
        logging.info("consecutives are: {}".format(consecutives))

        for c in consecutives:
            if len(c) >= num_salads:
                for i in range(len(c) - num_salads + 1):
                    start_index = i
                    end_index = start_index + num_salads
                    logging.info("consecutive of length {}: \
                            {}".format(num_salads, c[start_index: end_index]))
                    cost = sum(c[start_index: end_index])
                    # set solution to cost of this consecutive sequence if it is the first solution or if it
                    # is better than previous solutions
                    if spent == 0 or cost < spent:
                        spent = cost

    result = {"result": spent}
    logging.info("My result :{}".format(result))
    return json.dumps(result);

