from stock_statistics import Statistics
import matplotlib.pyplot as plt
import pandas as pd

prices_data = pd.read_csv("prices.txt", delim_whitespace=True, header=None)
stats = Statistics(prices_data)

# Plot stock up to specified day.
def plot_stock(stock_num: int, day: int = stats.num_days):
    x_axis = list(range(day))
    plt.plot(x_axis, stats.prices_data[stock_num], label = "stock " + str(stock_num))

# Plots the moving average for specified stock with required shift.
def plot_moving_avg(stock_num: int, n: int,  end_day: int = stats.num_days):
    x_axis = [i + n - 1 for i in range(len(stats.complete_moving_avg(stock_num, n)))] # Handles translation of x axis.
    plt.plot(x_axis, stats.complete_moving_avg(stock_num, n, stats.num_days), label = "avg " + str(n))
 
# Testing
stock_num = 0
plot_stock(stock_num)
best_coef = -2
best_comparison_stock = None
for n in range(100):
    if n == stock_num:
        continue

    coef = stats.lagg_corr_coefficient(stock_num, n, 3)
    if best_coef < coef:
        best_coef = coef
        best_comparison_stock = n

print(best_comparison_stock)
print(best_coef)
plot_stock(best_comparison_stock)



plt.legend(loc = 9)
plt.show()

# Interesting stock numbers: 60 downward trend, 80 downward trend, 90 upward trendline at end
# 66 downward trendline. final price is touching the line.
# 67 same as 66

