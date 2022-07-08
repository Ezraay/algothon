import numpy as np
from stock_statistics import Statistics
from stock_strategy import Strategy

nInst=100
currentPos = np.zeros(nInst)

def getMyPosition (prcSoFar):
    global currentPos
    # Build your function body here

    stats = Statistics(prcSoFar)
    strat = Strategy(stats)

    return strat.new_pos(0.02, 5, 0)


    
