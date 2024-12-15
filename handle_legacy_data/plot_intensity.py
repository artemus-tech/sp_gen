import os

import numpy as np
import scipy


results = {
    'res_auto_save/shape3.0_scale=2.5/excess=1.0/sp_res/model_mean_intensshape3.0_scale=2.5_n=30000_rmax=37.4292698954_rmin=0.0733978343688_R=656.066997483_NC=0.1_excess=1.0_q[0.02,5.0].txt':30000,
    'res_auto_save\shape3.0_scale=2.5\C=0.01\sp_res\model_mean_intensshape3.0_scale=2.5_n=50000_NC=0.1_excess=1.005_C=0.01_q[0.02,5.0].txt':50000 ,
#    'res_auto_save/shape3.0_scale=2.5/C=0.01/sp_res/model_mean_intensshape3.0_scale=2.5_n=50000_NC=0.1_excess=1.005_C=0.01_q[0.02,5.0].txt':50000,
    'res_auto_save/shape3.0_scale=2.5/excess=1.006/sp_res/model_mean_intensshape3.0_scale=2.5_n=100000_rmax=47.3605056769_rmin=0.0853941789977_R=977.477729143_NC=0.1_excess=1.006_q[0.02,5.0].txt':100000
}

import matplotlib.pyplot as plt

markers = ['ro-', 'b--','g^-', 'kD-']

# Create the plot
plt.figure(figsize=(10, 6))
i=0
for k,v in results.items():
    data= np.loadtxt(os.path.join("C:/", k))
    # Plot each curve with a label
    plt.plot(data[:,0],data[:,1]/v,  markers[i], label="I(q)",markersize=i+1)
    i+=1

# Add labels, legend, and grid
plt.title("Four Curves on the Same Graph")
plt.xlabel("x")
plt.ylabel("y")
plt.loglog()
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

