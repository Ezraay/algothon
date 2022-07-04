import numpy as np
import pandas as pd

prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
num_stocks = len(prices_data.columns)
num_days = len(prices_data[0])

variances = [np.var(prices_data[i]) for i in range(num_stocks)]

# Returns variance of specified stock.
def variance(stock_num: int):
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

# Returns list of "active" resistances. An active resistance is a resistance
# that has not been violated. List is implicitly ascending. At most one resistance
# will be retrieved per interval.
def active_resistances(stock_num: int, interval_size: int, remove_last: bool = True):
    stock_price = list(prices_data[stock_num]) # Stock price on each day.
    values = [stock_price[0]] # List of the resistances.
    num_intervals = num_days // interval_size
    if num_days % interval_size != 0:
        num_intervals += 1

    # Builds values.
    for i in range(num_intervals):
        # Finds minimum stock value in interval.
        day = i * interval_size
        min = stock_price[day]
        for j in range(interval_size):
            day = i * interval_size + j

            if(day >= num_days):
                break
            
            if stock_price[day] < min:
                min = stock_price[day]

        # Removes violated resistances.
        while len(values) > 0 and values[-1] > min:
            values.pop()
        
        values.append(min)
    
    # Remove last probably desired since last resistance is often just the final stock price.
    if remove_last:
        values.pop()

    return values







