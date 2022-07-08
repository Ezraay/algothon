from stock_statistics import Statistics
from stock_predictions import Predictions

prev_pos = None

class Strategy:
    def __init__(self, stat_obj: Statistics):
        self.pred = Predictions(stat_obj)

    # 0.02, 

    def stock_pos(self, stock_num: int, required_return, primary_confidence_threshold, secondary_confidence_threshold, threshold = 0.05 ):
        previous_pos = 0
        if prev_pos != None:
            previous_pos = prev_pos[stock_num]

        if self.pred.stats.num_days < 150:
            return 0

        x = self.pred.expected_ppc_from_lagged_corr_coefficients(stock_num, 1, threshold)
        er = x[0]
        confidence = x[1]
        pos = 0
        
        if confidence > primary_confidence_threshold:
            if er > required_return:
                pos = 10000
            elif er < -required_return:
                pos = -10000

        if prev_pos is not None:
            if er > 0 and previous_pos > 0 and confidence > secondary_confidence_threshold:
                pos = previous_pos
            elif er < 0 and previous_pos < 0 and confidence > secondary_confidence_threshold:
                pos = previous_pos

        print(pos, confidence)

        return pos

    
    def new_pos(self, required_return, primary_confidence_threshold, secondary_confidence_threshold):
        global prev_pos
        prev_pos = [self.stock_pos(i, required_return, primary_confidence_threshold, secondary_confidence_threshold) for i in range(100)]
        return prev_pos

def reset_prev_pos():
    global prev_pos
    prev_pos = None


