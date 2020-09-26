import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def factorial(n):
    factorial = 1
    if int(n) >= 1:
        for i in range(1, int(n)+1):
            factorial = factorial * i
    return factorial

def spaces_arrangement(seats, num_spaces):
    return factorial(seats+num_spaces-1) / (factorial(num_spaces-1)* factorial(seats))
  
# def solve(seats, distancing, people):
#     # for case where people at both ends
#     sum = seats - people # sum of seats that are empty
#     num = people - 1 # num of spaces
#     mem = [[0 for i in range(num + 1)] for j in range(sum + 1)]
#     logging.info(mem)
#     logging.info(mem[0][0])
#     recurse(sum, num, distancing, mem)
#     # mem = filter_invalid(mem, distancing)
#     logging.info(mem)
#     # for case where one person at one end
#     sum = seats - people # sum of seats that are empty
#     num = people # num of spaces
#     mem = [[0 for i in range(num + 1)] for j in range(sum + 1)]
#     logging.info(mem)
#     recurse(sum, num, distancing, mem)
#     # mem = filter_invalid(mem, distancing)
#     logging.info(mem)
#     return mem

# def filter_invalid(ls, space):
#     ls = list(filter(lambda x: None not in x, ls))
#     # ls = [x for x in ls if y for y in x if y >= space]
#     return ls

# def recurse(sum, num, space, mem):
#     if num == 1:
#         # solved
#         mem[sum][num] = 1
#         return 
#     else:
#         for i in range(sum):
#             # if mem[sum - i][num - 1] != 0:
#             #     # if in memory
#             #     mem[sum][num] += (mem[sum - i][num - 1])
#             # else: 
#             #     # else calculate and store to memory
#             recurse(sum - i, num - 1, space, mem)
#             # if mem[sum - i][num - 1] != 0:
#             mem[sum][num] += (mem[sum - i][num - 1])
#         return

@app.route('/social_distancing', methods=['POST'])
 
def social_distance():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");
    logging.info("tests sent for evaluation {}".format(tests))
    result = 0
    answer = {
        "answers": {}
    }
    # result = solve(tests["0"]["seats"], tests["0"]["spaces"], tests["0"]["people"])

    for k,v in zip(tests.keys(), tests.values()):
        seats = v["seats"]
        people = v["people"]
        spaces = v["spaces"]
        # logging.info("ref: {}".format(spaces_arrangement(seats - people - spaces * (people - 1), people)))
        # case if people seating at both ends
        result += spaces_arrangement(seats - people - spaces * (people - 1), people - 1)
        logging.info("result: {}".format(result))
        # case if one person seated at an end
        # result += spaces_arrangement(seats - people - spaces * (people - 1), people)
        result += spaces_arrangement(seats - people - spaces * (people - 1) - 1, people) * 2
        logging.info("result: {}".format(result))
        # case if none seated at ends
        result += spaces_arrangement(seats - people - spaces * (people - 1) - 2, people + 1)
        logging.info("result: {}".format(result))
        answer["answers"][k] = result
        result = 0
    logging.info("My result :{}".format(answer))
    return jsonify(answer);



