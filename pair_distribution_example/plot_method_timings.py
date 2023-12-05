import matplotlib.pyplot as plt
import pandas as pd

# Read data from the file
data = pd.read_csv("timing_results.csv", delim_whitespace=True)

# Plotting
for column in data.columns[1:]:  # Skip the first column 'N'
    plt.plot(data['N'], data[column], label=column)

plt.xlabel("N time steps")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time Comparison")
plt.legend()

plt.xscale('log')
plt.yscale('log')

plt.savefig('method_timings.png', dpi=400)
# plt.show()