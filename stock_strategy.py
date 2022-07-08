from stock_statistics import Statistics
from stock_predictions import Predictions


class Strategy:
    def __init__(self, stat_obj: Statistics):
        self.pred = Predictions(stat_obj)

    def stock_pos(self, stock_num: int):
        if self.pred.stats.num_days < 150:
            return 0

        x = self.pred.expected_ppc_from_lagged_corr_coefficients(stock_num, 1, 0.05)
        er = x[0]
        confidence = x[1]
        pos = 0
        if er > 0.02:
            pos = 10000
        elif er < -0.02:
            pos = -10000

        if confidence < 3.5:
            pos = 0
        return pos

    
    def new_pos(self):
        return [self.stock_pos(i) for i in range(100)]


