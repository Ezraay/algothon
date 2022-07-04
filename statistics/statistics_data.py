import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
num_stocks = len(prices_data.columns)
num_days = len(prices_data[0])

variances = [np.var(prices_data[i]) for i in range(num_stocks)]

def get_variance(stock_num: int):
    return variances[stock_num]

# Returns moving avg of size n at specified day.
# Returns average if n greater than or equal to day_num.
def moving_average(stock_num: int, n: int, day_num: int):
        start_day = day_num - n + 1 # First day of running avg calculation
        # In this case the total avg is returned.
        if start_day < 0:
            start_day = 0
        return np.average(list(prices_data[stock_num][start_day:day_num + 1]))

# Returns a list of the moving avg of size n at every day up to end_day.
def complete_moving_avg(stock_num: int, n: int,  end_day: int = num_days):
    return [moving_average(stock_num, n, i) for i in range(n - 1, end_day)]




