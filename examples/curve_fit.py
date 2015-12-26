import numpy as np
from crepe import normal
import matplotlib.pyplot as plt

n = normal.optimize()
shift = 0.

# Function to be simulated
def f(x,a,b):
    return a*np.exp(-b*x)

# Generating noisy data
N = 100
true_a = 1.0
true_b = 0.5
noise_sigma = 0.2
x = np.linspace(0.0,10.0,N)
y = np.array([f(xk,true_a,true_b)+np.random.normal(scale=noise_sigma) for xk in x])
true_y = np.array([f(xk,true_a,true_b) for xk in x])
data = np.array([[x[i],y[i]] for i in range(N)])

#plt.plot(x,y,'.')
#plt.plot(x,true_y)
#plt.show()

"""
# This section saves the data to the file data.dat
f = open('data.dat','rwx+')
f.truncate()
for i in range(N):
    f.write("%.5E\t\t%.5E\t\t%.5E\n" % (x[i],y[i],true_y[i]))
f.close()
"""

# Now, let's guess a and b
p_min = np.array([0.1,0.01])       # Parameters minima
p_max = np.array([5.0,1.0])     # Parameters maxima
p_mean = (p_min + p_max)/2.         # Parameters means
p_sigma = (p_max - p_min)/2.        # Parameters standard deviations

# Here a few tweaks that I want to use
a = 0.9                       # Smoothing factor, between 0 and 1
b = 0.1                      # Smoothing power, between ~1/10 and 1/5
r = 0.05                         # Sample quantile that will define elite

# The performance function - probably the hardest part
def perf(p):
    y_p = np.array([f(xk,p[0],p[1]) for xk in x])
    R = (data[:,1]-y_p)**2
    Rmean = np.sum(R)/N
    return Rmean*(1./N)*np.sum((R-Rmean)**2)

new_p_mean,new_p_sigma = n.estimate(
    perf,p_mean,p_sigma,alpha=a,beta=b,rho=r,verbose=True
    )
print('a = %.3f p/m %.3f' % (new_p_mean[0],new_p_sigma[0]))
print('b = %.3f p/m %.3f' % (new_p_mean[1],new_p_sigma[1]))

estim_y = np.array([f(xk,new_p_mean[0],new_p_mean[1]) for xk in x])
plt.plot(x,y,'.',label='Noisy signal')
plt.plot(x,true_y,'r',label='True signal')
plt.plot(x,estim_y,'g',label='Fitted signal')
plt.legend()
plt.show()
