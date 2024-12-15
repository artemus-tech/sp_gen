import os

import matplotlib.pyplot as plt
import numpy as np

result_dict = {
    'C:\\res_auto_save\\shape3.0_scale=2.5\\C=0.01\\sp_res':50000,
    'C:\\res_auto_save\\shape3.0_scale=2.5\\excess=1.0\\sp_res':30000,
    'C:\\res_auto_save\\shape3.0_scale=2.5\\excess=1.006\\sp_res':100000,

}
markers = ['ro-', 'b--','g^-', 'kD-']

# Create the plot
plt.figure(figsize=(10, 6))
i = 0
for k, v in result_dict.items():
    data = np.loadtxt(os.path.join("C:/", k, 'sem_meant.txt'))
    # Plot each curve with a label
    plt.plot(data[:, 0], data[:, 2] / data[:,1], markers[i], label=f"I(q){v}", markersize=i + 1)
    i += 1

# Add labels, legend, and grid
plt.title("Four Curves on the Same Graph")
plt.xlabel("q,nm")
plt.ylabel("deltaI,arb units")
plt.xscale('log')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()







