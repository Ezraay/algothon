from stock_statistics import Statistics
from stock_predictions import Predictions
import pandas as pd

prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
stats = Statistics(prices_data)
pred = Predictions(stats)

stock_num = 7

sum = 0
thresh = 0.5
for n in range(100):
    fdp = stats.prices_data[n][248]
    ldp = stats.prices_data[n][249]
    lcc = stats.lagg_corr_coefficient(stock_num, n, 1)
    ppc = stats.percent_price_change(n, stats.num_days - 2)
    sppc = stats.std_percent_price_change(n)
    
    print("first day price   : ", fdp)
    print("last day price    : ", ldp)
    print("lagged corr coef  :", lcc)
    print("percnt prc change :",ppc)
    print("std prcnt prc chng:", sppc)
    print("")

prediction = pred.expected_ppc_from_lagged_corr_coefficients(stock_num, 1, thresh)
print(prediction)


    
