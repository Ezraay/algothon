from stock_statistics import Statistics
import numpy as np

def lagg_corr_coefficient(l1: list, l2: list, n: int):
    # Ensures indicator exists.
    if n >= len(l1) / 2 and n >= len(l2) / 2:
        return None

    l1 = l1[:-n]
    l2 = l2[n:]
    return np.corrcoef(l1, l2)[0][1]

class Predictions:
    def __init__(self, stat_obj: Statistics):
        self.stats = stat_obj

    # Determines expected percent price change over n day period for some stock
    # from lagged correlation coefficients of other stocks and their observed ppc.
    # ppc -> percent price change.
    def expected_ppc_from_lagged_corr_coefficients(self, stock_num: int, n: int, threshold: float):
        # Builds list l containing tuples of ppc in terms of std of stock and lagged corr coef with specified stock.
        l = [] 
        appc1 = self.stats.all_percent_price_changes(stock_num)
        for i in range(self.stats.num_stocks):
            if i == stock_num:
                continue

            appc2 = self.stats.all_percent_price_changes(i)
            lcc = lagg_corr_coefficient(appc1, appc2, n)
            if abs(lcc) < threshold:
                continue
            
            ppc_in_std = self.stats.percent_price_change(i, n) / self.stats.std_percent_price_change(i,n)
            l.append((ppc_in_std, lcc))
        
        ppc_x_lcc_sum = 0
        abs_lcc_sum = 0 # Absolute sum of lagg correlations. Used for determining confidence in estimation.
        for i in range(len(l)):
            ppc_x_lcc_sum += l[i][0] * l[i][1]
            abs_lcc_sum += abs(l[i][1])

        if abs_lcc_sum == 0:
            return (0, 0)

        expected_ppc_in_std = ppc_x_lcc_sum / abs_lcc_sum  # expected ppc in terms of standard deviation.
        er = expected_ppc_in_std / self.stats.std_percent_price_change(stock_num)
        return (er, abs_lcc_sum)




        
        

