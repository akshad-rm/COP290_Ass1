
import pandas as pd
from datetime import date
from jugaad_data.nse import NSELive
import matplotlib.pyplot as plt

n = NSELive()
q = n.chart_data("SBIN")
r =n.stock_quote("SBIN")

xy_coordinates = q["grapthData"]

# Transpose the list to separate x and y values
x_values, y_values = zip(*xy_coordinates)

# Plot the graph
if r["priceInfo"]["change"] < 0:
    plt.plot(x_values, y_values, linestyle='-',color="red")
else:
    plt.plot(x_values, y_values, linestyle='-',color="green")


# Add labels and title
plt.xlabel('')
plt.ylabel('Stock Price')
plt.title('SBIN')
plt.gca().set_facecolor('#333')
# Show the plot
plt.show()