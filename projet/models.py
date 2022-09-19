from projet.algos import algoMinili, algoBalasHammer
from projet.steppingStone import stepping


def miniLi(l, dataY, dataX):
    z, cost = algoMinili(tuple(l), dataY, dataX)
    zB, costB = algoBalasHammer(tuple(l), dataY, dataX)
    resU, resC, resLink , zMin= stepping(l, dataX, dataY, cost.tolist())
    return resU, resC, resLink, zMin, z


def balasHammer(l, dataY, dataX):
    z, cost = algoBalasHammer(tuple(l), dataY, dataX)
    resU, resC, resLink, zMin = stepping(l, dataX, dataY, cost.tolist())
    return resU, resC, resLink, zMin, z
