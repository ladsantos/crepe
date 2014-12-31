import numpy as np
from crepe import optimize
import matplotlib.pyplot as plt

n = optimize.normal()

# Function to be simulated
def f(x,a,b):
    return a*np.sin(x)+b

# Generating noisy data
N = 500
true_a = 2.0
true_b = 10.0
noise_sigma = 1.0
x = np.linspace(0.0,10.0,N)
y = np.array([f(xk,true_a,true_b)+np.random.normal(scale=noise_sigma) for xk in x])
true_y = np.array([f(xk,true_a,true_b) for xk in x])
data = np.array([[x[i],y[i]] for i in range(N)])

# Now, let's guess a and b
p_min = np.array([5.0,2.0])       # Parameters minima
p_max = np.array([10.0,10.0])     # Parameters maxima
p_mean = (p_min + p_max)/2.         # Parameters means
p_sigma = (p_max - p_min)/2.        # Parameters standard deviations

# Here a few tweaks that I want to use
a = 0.7                       # Smoothing factor, between 0 and 1
b = 0.14                       # Smoothing power, between ~5 and ~10
c = 0.1                     # Lower limit for the change in parameter estimation
k = 20                        # Max number of iterations
r = 0.1                         # Sample quantile that will define elite

# The performance function - probably the hardest part
def perf(p):
    R = (data[:,1]-f(data[:,0],p[0],p[1]))**2
    Rmean = np.sum(R)/N
    return Rmean*(1./N)*np.sum((R-Rmean)**2)

new_p_mean,new_p_sigma = n.estimate(perf,p_mean,p_sigma,alpha=a,beta=b,c_limit=c,k_max=k,rho=r)
print 'a = %.3f p/m %.3f' % (new_p_mean[0],new_p_sigma[0])
print 'b = %.3f p/m %.3f' % (new_p_mean[1],new_p_sigma[1])

estim_y = np.array([f(xk,new_p_mean[0],new_p_mean[1]) for xk in x])
plt.plot(x,y,'.',label='Noisy signal')
plt.plot(x,true_y,'r',label='True signal')
plt.plot(x,estim_y,'g',label='Fitted signal')
plt.legend()
plt.show()