import numpy as np
import pandas as pd
import time
from stock_statistics import Statistics
import stock_strategy
from stock_strategy import Strategy 
import matplotlib.pyplot as plt


nInst=100
currentPos = np.zeros(nInst)
nt = 0

# Commission rate
commRate = 0.0025 # was 0.0050

# Dollar position limit (maximum absolute dollar value of any individual stock position)
dlrPosLimit = 10000

timeOut=600 

def loadPrices(fn):
    global nt, nInst
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices.txt"
prcAll = loadPrices(pricesFile)


def getPosition (prcSoFar, req_return, prim_conf_thresh, sec_conf_thresh):
    global currentPos

    stats = Statistics(prcSoFar)
    strat = Strategy(stats)

    return strat.new_pos(req_return, prim_conf_thresh, sec_conf_thresh)


def calcPL(prcHist, req_return, prim_conf_thresh, sec_conf_thresh):
    global tStart
    cash = 0
    curPos = np.zeros(nInst)
    totDVolume = 0
    frac0 = 0.
    frac1 = 0.
    value = 0
    todayPLL = []
    (_,nt) = prcHist.shape
    tNow = time.time()
    for t in range(1,nt+1): 
        prcHistSoFar = prcHist[:,:t]
        # no trades on the very last price update, only before the last update
        newPosOrig = curPos
        tNow = time.time()
        tRunning = tNow - tStart
        #print ("tRunning: %.4lf" % tRunning)
        if (t < nt) and (tRunning <= timeOut):
            newPosOrig = getPosition(prcHistSoFar, req_return, prim_conf_thresh, sec_conf_thresh)
            # otherwise keep the same desired positions
        if (tRunning > timeOut):
            print ("TIME OUT [ %.3lf > %lf]!" % (tRunning, timeOut))
        curPrices = prcHistSoFar[:,-1] #prcHist[:,t-1]
        posLimits = np.array([int(x) for x in dlrPosLimit / curPrices])
        newPos = np.array([int(p) for p in np.clip(newPosOrig, -posLimits, posLimits)])
        deltaPos = newPos - curPos
        dvolumes = curPrices * np.abs(deltaPos)
        dvolume = np.sum(dvolumes)
        totDVolume += dvolume
        comm = dvolume * commRate
        cash -= curPrices.dot(deltaPos) + comm
        curPos = np.array(newPos)
        posValue = curPos.dot(curPrices)
        todayPL = cash + posValue - value
        todayPLL.append(todayPL)
        value = cash + posValue
        ret = 0.0
        if (totDVolume > 0):
            ret = value / totDVolume
    pll = np.array(todayPLL)
    (plmu,plstd) = (np.mean(pll), np.std(pll))
    annSharpe = 0.0
    if (plstd > 0):
        annSharpe = 16 * plmu / plstd
    return (plmu, ret, annSharpe, totDVolume)


def single_test(er, prim_conf_thresh, sec_conf_thresh):
    tStart = time.time()
    (meanpl, ret, sharpe, dvol) = calcPL(prcAll, er, prim_conf_thresh, sec_conf_thresh)
    tEnd = time.time()
    tRun = tEnd - tStart
    profit = ret * dvol
    return [profit, meanpl, ret, sharpe]

xs =[]
profits = []
meanpls = []
rets = []
sharpes = []




for prim_conf_thresh in [4.5, 4.75, 5, 5.25, 5.5, 5.75, 6, 6.25, 6.5, 6.75, 7]:
    print("")
    print(prim_conf_thresh)

    xs.append(prim_conf_thresh)

    tStart = time.time()
    results = single_test(0.02, prim_conf_thresh, 0)
    tEnd = time.time()
    tRun = tEnd - tStart

    profits.append(results[0])
    meanpls.append(results[1])
    rets.append(results[2])
    sharpes.append(results[3])

    stock_strategy.reset_prev_pos()

plt.plot(xs, sharpes)
plt.show()

