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


def helper(timeRem, books, currIndex, currMax, memo, currList):
    if currIndex not in memo.keys():
        if timeRem < 0:
            index = currList.pop(len(currList) - 1)
            memo[currIndex] = (currMax - 1, currList)
        elif timeRem == 0 or currIndex == len(books) - 1:
            memo[currIndex] = (currMax, currList)
        else:
            currList.append(currIndex)
            (maxI, currListI) = helper(timeRem - books[currIndex], books, currIndex + 1,
                                       currMax + 1, memo, currList)
            logger.info("maxI " + str(maxI) + str(currListI))
            logger.info("currIndex: " + str(currIndex))
            (maxJ, currListJ) = helper(timeRem, books, currIndex + 1, currMax, memo, currList)
            logger.info("maxJ " + str(maxJ) + str(currListJ))
            if maxI > maxJ:
                memo[currIndex] = (maxI, currListI)
            else:
                memo[currIndex] = (maxJ, currListJ)
        logger.info("memo[currIndex]: " + str(memo[currIndex]))
    return memo[currIndex]


def findMaxBooksThatFitIntoTime(time, books, firstBookAboveTime):
    memo = {}
    helper(time, books[:firstBookAboveTime], 0, 0, memo, [])
    return memo[firstBookAboveTime - 1]


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
            logger.info("firstBook above time:"  + str(firstBookAboveTime))
            logger.info("time" + str(time))
            (maxBooks, listOfBooksToRemove) = findMaxBooksThatFitIntoTime(time, books, firstBookAboveTime)
            optimalSolution += maxBooks
            logger.info("optimal solution: " + str(optimalSolution))
            logger.info("books" + str(books))
            valueOfBooksToRemove = [books[index] for index in listOfBooksToRemove]
            logger.info("valueOfBooksToRem: " + str(valueOfBooksToRemove))
            for value in valueOfBooksToRemove:
                books.remove(value)



    return optimalSolution
