import numpy as np
import pandas as pd

class Statistics:

    prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
    num_stocks = len(prices_data.columns)
    num_days = len(prices_data[0])

    def __init__(self, prc_data):
        self.prices_data = prc_data
        self.num_stocks = len(self.prices_data.columns)
        self.num_days = len(self.prices_data[0])

    # Finds average of price changes of pairs of adjacent days. This is a measure of volatility.
    # Can find average for multi day movements through n.
    def abs_average_price_change(self, stock_num: int, n: int = 1, start_day: int = 0, end_day: int = None):
        if end_day == None:
            end_day = self.num_days - 1

        stock_price = list(self.prices_data[stock_num]) # Stock price on each day.
        price_change = [np.abs(stock_price[i] - stock_price[i - 1]) for i in range(0, end_day + 1, n)]
        return np.average(price_change)

    # Specifies price difference that signifies violated resistance or support for a given stock.
    def violation_value(self, stock_num: int, factor1: int = 1, factor2: int = 200, day: int = 0):
        avg_3_day_movement = self.abs_average_price_change(stock_num, 3)
        stock_price = self.prices_data[stock_num][day]
        return np.minimum(factor1 * avg_3_day_movement, stock_price / factor2)

    # Checks if violation has occurred at day for a stock. True then violation.
    def test_violation(self, stock_num: int, day: int, value: int, violation_value: int):
        return np.abs(self.prices_data[stock_num][day] - value) > violation_value

    # Test if value at day is larger than neighbouring days.
    def test_peak(self, stock_num: int, day: int, n: int, max_day: int = None):
        if max_day == None:
            max_day = self.num_days - 1
        stock_prices = list(self.prices_data[stock_num]) # Stock price on each day.

        for i in range(1, n + 1):
            if day + i <= max_day and stock_prices[day + i] > stock_prices[day]:
                return False
            if day - i >= 0 and stock_prices[day - i] > stock_prices[day]:
                return False

        return True

    # Test if value at day is lesser than neighbouring days.
    def test_trough(self, stock_num: int, day: int, n: int, max_day: int = None):
        if max_day == None:
            max_day = self.num_days - 1
        stock_prices = list(self.prices_data[stock_num]) # Stock price on each day.

        for i in range(1, n + 1):
            if day + i <= max_day and stock_prices[day + i] < stock_prices[day]:
                return False
            if day - i >= 0 and stock_prices[day - i] < stock_prices[day]:
                return False

        return True

    # Returns moving avg of size n at specified day.
    # Returns average if n greater than or equal to day_num.
    def moving_average(self, stock_num: int, n: int, day_num: int):
            start_day = day_num - n + 1 # First day of running avg calculation
            # In this case the total avg is returned.
            if start_day < 0:
                start_day = 0
            return np.average(list(self.prices_data[stock_num][start_day:day_num + 1]))

    # Returns a list of the moving avg of size n at every day up to end_day.
    def complete_moving_avg(self, stock_num: int, n: int,  end_day: int = num_days):
        return [self.moving_average(stock_num, n, i) for i in range(n - 1, end_day)]

    # Returns list of "active" supports. An active support is a support
    # that has not been violated. List is implicitly ascending. At most one support
    # will be retrieved per interval. Min_dist is the minimum distance between supports.
    # If empty list is returned then the stock price has an all time low in the final interval.
    # Typically only the last support is relevant.
    def active_supports(self, stock_num: int, interval_size: int,  min_dist: int, end_day: int = num_days):
        stock_prices = list(self.prices_data[stock_num]) # Stock price on each day.
        supports = [(stock_prices[0], 0)] # List of the support values and day of occurrance.
        num_intervals = end_day // interval_size

        if self.num_days % interval_size != 0:
            num_intervals += 1

        prev_support_day = -min_dist
        # Builds values.
        for i in range(num_intervals):
            if len(supports) > 0 and i != 0:
                prev_support_day = supports[-1][1]
            # Finds minimum stock value in interval.
            day = i * interval_size
            min = stock_prices[day]
            min_day = day  # Day that maximum value (resistance) occurs in interval.
            for j in range(interval_size):
                day = i * interval_size + j
                if(day >= end_day):
                    break
                
                if stock_prices[day] < min:
                    min = stock_prices[day]
                    min_day = day

            # Removes violated supports.
            while len(supports) > 0 and supports[-1][0] > min:
                supports.pop()

            # Updates prev_support_day
            if len(supports) > 0 and i != 0:
                prev_support_day = supports[-1][1]      
            else:
                prev_support_day = -min_dist
    
            # Ensures no support in final interval.
            if i < num_intervals - 1:
                # Appends min to values if sufficient and updates prev_support_day.
                dist = min_day - prev_support_day
                if self.test_trough(stock_num, min_day, 3) and (len(supports) == 0 or dist >= min_dist):
                    supports.append((min, min_day))

        # Ensures no support in first interval.
        if len(supports) > 0 and supports[0][1] < interval_size:
            supports = supports[1:]

        values = [supports[i][0] for i in range(len(supports))] # Collects the prices of each support.
        return values

    # Returns list of "active" resistances. An active resistance is a resistance
    # that has not been violated. List is implicitly descending. At most one resistance
    # will be retrieved per interval. Min_dist is the minimum distance between resistances.
    # If empty list is returned then the stock price has an all time low in the final interval.
    # Typically only the last support is relevant.
    def active_resistances(self, stock_num: int, interval_size: int,  min_dist: int, end_day: int = num_days):
        stock_prices = list(self.prices_data[stock_num]) # Stock price on each day.
        resistances = [(stock_prices[0], 0)] # List of the support values and day of occurrance.
        num_intervals = end_day // interval_size

        if self.num_days % interval_size != 0:
            num_intervals += 1

        prev_resistance_day = -min_dist
        # Builds values.
        for i in range(num_intervals):
            if len(resistances) > 0 and i != 0:
                prev_resistance_day = resistances[-1][1]
            # Finds minimum stock value in interval.
            day = i * interval_size
            max = stock_prices[day]
            max_day = day  # Day that maximum value (resistance) occurs in interval.
            for j in range(interval_size):
                day = i * interval_size + j
                if(day >= end_day):
                    break
                
                if stock_prices[day] > max:
                    max = stock_prices[day]
                    max_day = day

            # Removes violated resistances.
            while len(resistances) > 0 and resistances[-1][0] < max:
                resistances.pop()

            # Updates prev_support_day
            if len(resistances) > 0 and i != 0:
                prev_resistance_day = resistances[-1][1]      
            else:
                prev_resistance_day = -min_dist

            # Appends min to values if sufficient and updates prev_resistance_day.
            dist = max_day - prev_resistance_day
            if self.test_peak(stock_num, max_day, 3) and (len(resistances) == 0 or dist >= min_dist):
                resistances.append((max, max_day))

        # Ensures no resistance in first interval.
        if len(resistances) > 0 and resistances[0][1] < interval_size:
            resistances = resistances[1:]

        values = [resistances[i][0] for i in range(len(resistances))] # Collects the prices of each support.
        return values

    # Finds number of intervals that a support is tested. If interval yields min value
    # less than specified support value then support may no longer be tested.
    # This is a measure of the strength and validity of the support.
    def num_support_tests(self, stock_num: int, support: int, interval_size: int, end_day: int = num_days):
        stock_price = list(self.prices_data[stock_num]) # Stock price on each day.
        num_intervals = end_day // interval_size
        violation_val = self.violation_value(stock_num) # Range that specifies successful test of support.
        cnt = 0 # Number of successful tests of support.

        if self.num_days % interval_size != 0:
            num_intervals += 1

        # Determines cnt.
        for i in reversed(range(num_intervals)):
            day = i * interval_size
            for j in range(interval_size):
                day = i * interval_size + j
                if(day >= end_day):
                    break
                elif np.abs(stock_price[day] - support) < violation_val:
                    cnt += 1
                    break
                elif stock_price[day] < support:
                    return cnt

        return cnt



    










