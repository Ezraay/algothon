import statistics_data as sd
import matplotlib.pyplot as plt

# Plot stock up to specified day.
def plot_stock(stock_num: int, day: int = sd.num_days):
    x_axis = list(range(day))
    plt.plot(x_axis, sd.prices_data[stock_num])

# Plots the moving average for specified stock with required shift.
def plot_stock_moving_avg(stock_num: int, n: int,  end_day: int = sd.num_days):
    x_axis = [i + n - 1 for i in range(len(sd.complete_moving_avg(stock_num, n)))] # Handles translation of x axis.
    plt.plot(x_axis, sd.complete_moving_avg(stock_num, n, sd.num_days), label = "avg " + str(n))

# Plots horizontal lines representing the active resistances for the stock and specified interval.
def plot_active_resistances(stock_num: int, interval: int):
    for i in sd.active_resistances(stock_num, interval):
        plt.axhline(i)


plot_stock(9)
plot_active_resistances(9, 30)

plt.legend(loc = 9)

plt.show()