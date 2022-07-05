import statistics 
import matplotlib.pyplot as plt
import pandas as pd

prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
stats = statistics.Statistics(prices_data)

# Plot stock up to specified day.
def plot_stock(stock_num: int, day: int = stats.num_days):
    x_axis = list(range(day))
    plt.plot(x_axis, stats.prices_data[stock_num])

# Plots the moving average for specified stock with required shift.
def plot_moving_avg(stock_num: int, n: int,  end_day: int = stats.num_days):
    x_axis = [i + n - 1 for i in range(len(stats.complete_moving_avg(stock_num, n)))] # Handles translation of x axis.
    plt.plot(x_axis, stats.complete_moving_avg(stock_num, n, stats.num_days), label = "avg " + str(n))

# Plots horizontal lines representing the active supports for the stock and specified interval.
def plot_active_supports(stock_num: int, interval: int, min_dist: int):
    for i in stats.active_supports(stock_num, interval, min_dist):
        plt.axhline(i, color = 'g')

# Plots horizontal lines representing the active resistances for the stock and specified interval.
def plot_active_resistances(stock_num: int, interval: int, min_dist: int):
    for i in stats.active_resistances(stock_num, interval, min_dist):
        plt.axhline(i, color = 'r')    

# Testing
stock_num = 86
plot_stock(stock_num)
plot_active_supports(stock_num, 40, 25)
plot_active_resistances(stock_num, 40, 25)

print(stats.violation_value(stock_num))
if len(stats.active_supports(stock_num, 40, 25)):
    print(stats.num_support_tests(stock_num, stats.active_supports(stock_num, 40, 25)[-1], 15))

plt.legend(loc = 9)
plt.show()

# Interesting stock numbers: 60 downward trend, 80 downward trend, 90 upward trendline at end
# 66 downward trendline. final price is touching the line.
# 67 same as 66

