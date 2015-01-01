import numpy as np
from crepe import optimize
import matplotlib.pyplot as plt

n = optimize.normal()

# Importing data
data = np.loadtxt('data.dat',float,usecols=(0,1))
N = len(data[:,0])

# Function to be simulated
def f(x,a,b):
    return a*np.sin(x)+b

# The performance function: just a simple sum of the squared differences!
def perf(p):
    return np.sum((data[:,1]-f(data[:,0],p[0],p[1]))**2)

# Let's guess a and b (an interval that you think they could be inside)
p_min = np.array([5.0,2.0])     # Parameters minima
p_max = np.array([10.0,10.0])   # Parameters maxima
p_mean = (p_min + p_max)/2.     # Parameters means
p_sigma = (p_max - p_min)/2.    # Parameters standard deviations

# The estimation by CREPE is done in just one line:
new_p_mean,new_p_sigma = n.estimate(perf,p_mean,p_sigma)

# Printing and plotting the results
print 'a = %.3f p/m %.3f' % (new_p_mean[0],new_p_sigma[0])
print 'b = %.3f p/m %.3f' % (new_p_mean[1],new_p_sigma[1])
estim_y = np.array([f(xk,new_p_mean[0],new_p_mean[1]) for xk in data[:,0]])
plt.plot(data[:,0],data[:,1],'.',label='Noisy signal')
plt.plot(data[:,0],estim_y,'g',label='Fitted signal')
plt.legend()
plt.show()