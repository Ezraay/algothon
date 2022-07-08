import numpy as np

class Statistics:
    def __init__(self, prc_data):
        self.prices_data = prc_data
        self.num_stocks = 100 # test that this is 100
        self.num_days = len(prc_data[0])

    # Returns percent price change from some day to another day.
    def percent_price_change(self, stock_num: int, first_day: int, last_day: int = None):
        if last_day is None:
            last_day = self.num_days - 1

        stock_prices = self.prices_data[stock_num]
        price_difference = stock_prices[last_day] - stock_prices[first_day]
        return price_difference / stock_prices[first_day]

    def all_percent_price_changes(self, stock_num: int, last_day: int = None):
        if last_day is None:
            last_day = self.num_days - 1

        return [self.percent_price_change(stock_num, i - 1, i) for i in range(1, last_day)]
    
    # Returns standard deviation of price changes across n days.
    def std_percent_price_change(self, stock_num: int, n: int = 1):
        percent_price_changes = [self.percent_price_change(stock_num, i - 1, i + n - 1) for i in range(1, self.num_days)]
        return np.std(percent_price_changes)

    # Correlation coefficient between two stocks.
    def corr_coefficient(self, stock1_num: int, stock2_num: int):
        stock1_prices = self.prices_data[stock1_num]
        stock2_prices = self.prices_data[stock2_num]
        return np.corrcoef(stock1_prices, stock2_prices)[0][1]



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
    def moving_average(self, stock_num: int, day_num: int, n: int):
            start_day = day_num - n + 1 # First day of running avg calculation
            # In this case the total avg is returned.
            if start_day < 0:
                start_day = 0
            return np.average(list(self.prices_data[stock_num][start_day:day_num + 1]))

    # Returns a list of the moving avg of size n at every day up to end_day.
    def complete_moving_avg(self, stock_num: int, n: int,  end_day: int = None):
        if end_day == None:
            end_day = self.num_days - 1
        return [self.moving_average(stock_num, n, i) for i in range(n - 1, end_day)]

  
    






