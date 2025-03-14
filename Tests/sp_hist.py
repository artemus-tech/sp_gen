import numpy as np
import os
import scipy.special as sps
import matplotlib.pyplot as plt


plt.title("Histogram with non 'auto' bins")
shape=3.5
scale=2.0
r = np.random.gamma(shape,scale,100)

count, bins, ignored = plt.hist(r, 50, normed=True)
y = bins**(shape-1)*(np.exp(-bins/scale) / (sps.gamma(shape)*scale**shape))

plt.ylabel('f(R)')
plt.xlabel('R')

formula = r'$f(R) = R^{k-1}{\frac{-e^{R/\theta}}{\theta\Gamma(k) }}$'
#numf = formula.replace(r'\theta', str(scale))

plt.plot(bins, y, linewidth=2, color='r',label=formula)
plt.text(8.5, 0.1, r'$k=' + str(shape)+r'$' ,fontsize=32)
plt.text(8.5, 0.075, r'$\theta='+str(scale)+r'$',fontsize=32)
plt.legend(prop={'size': 32})
plt.show()
