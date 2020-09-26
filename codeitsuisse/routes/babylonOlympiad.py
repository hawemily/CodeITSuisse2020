import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_babylon_olympiad():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    noOfBooks = data["numberOfBooks"]
    numberOfDays = data["numberOfDays"]
    books = data["books"]
    days = data["days"]
    result = findOptimalSolution(books, days)
    logging.info("My result :{}".format(result))
    formattedResult = {"optimalNumberOfBooks": result}
    return json.dumps(formattedResult)


def findFirstIndexOfBookRequiringMoreThanTimetoComplete(time, books):
    for i in range(len(books)):
        if books[i] > time:
            return i
    return len(books) - 1


def helper(timeRem, books):
    n = len(books)
    table = [[0 for x in range(timeRem + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for time in range(timeRem + 1):
            if i == 0 or timeRem == 0:
                table[i][time] = 0
            elif books[i - 1] <= time:
                table[i][time] = max(table[i-1][time], table[i - 1][time - books[i - 1]] + 1)
                # logging.info("i: " + str(i) + " timeRem: " + str(time) + " table[i][time]: " + str(table[i][time]))
            else:
                table[i][time] = table[i - 1][time]

    finalMax = table[n][timeRem]
    logging.info("table: " + str(table[n][timeRem]))
    timeRemn = timeRem
    ls = []
    for i in range(n, 0, -1):
        if finalMax <= 0:
            break
        if finalMax == table[i-1][timeRemn]:
            continue
        else:
            ls.append(books[i - 1])
            finalMax -= 1
            timeRemn -= books[i - 1]

    return table[n][timeRem], ls


def findMaxBooksThatFitIntoTime(time, books, firstBookAboveTime):
    return helper(time, books[:firstBookAboveTime])


def findOptimalSolution(books, days):
    days.sort()
    books.sort()
    optimalSolution = 0
    for time in days:
        if len(books) == 0:
            break

        # find books requiring less than or equal to amt of time to read
        firstBookAboveTime = findFirstIndexOfBookRequiringMoreThanTimetoComplete(time, books)

        if firstBookAboveTime == 0:
            continue
        else:
            logger.info("firstBook above time:" + str(firstBookAboveTime))
            logger.info("time" + str(time))
            (maxBooks, listOfBooksToRemove) = findMaxBooksThatFitIntoTime(time, books, firstBookAboveTime)
            optimalSolution += maxBooks
            logger.info("optimal solution: " + str(optimalSolution))
            logger.info("books" + str(books))
            # valueOfBooksToRemove = [books[index] for index in listOfBooksToRemove]
            # logger.info("valueOfBooksToRem: " + str(valueOfBooksToRemove))
            for value in listOfBooksToRemove:
                books.remove(value)

    return optimalSolution
