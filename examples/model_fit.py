import numpy as np
import optimize
import matplotlib.pyplot as plt

n = optimize.normal()

# Emission lines wavelengths
lA = 6650.      # Element A
lB = 6300.      # Element B
lC = 7500.      # Element C

# True parameters
A_abund = 1.0E-3        # Abundance of element A
B_abund = 2.3E-4        # Abundance of element B
C_abund = 7.2E-6        # Abundance of element C
rot = 40.0              # Line spread parameter

noise_sigma = 0.1
N = 1000        # Number of datapoints

def DiracDelta(a,center,x):
    return np.exp(-(x-center)**2/a**2)/(a*np.sqrt(np.pi))

# Constants
K1 = 1.2E5
K2 = 2.9E5
K3 = 7.2E6

# The model
x = np.linspace(6000.,8000.,N)
def signal(x,A,B,C,r):
    y = K1*A*DiracDelta(r,lA,x) + K2*B*DiracDelta(r,lB,x) + K3*C*DiracDelta(r,lC,x)
    return y

# Creating the data
true_y = np.array([signal(xk,A_abund,B_abund,C_abund,rot) for xk in x])
noisy_y = np.array([yk+np.random.normal(scale=noise_sigma) for yk in true_y])
data = data = np.array([[x[i],noisy_y[i]] for i in range(N)])


# I want to estimate the values of the abundances of A, B and C and the line spread parameter
# Let's start by guessing them. Notice that there's a huge gap between our minima and maxima guesses
# This will probably cause CREPE to arrive at the maximum number of iterations.
# Even so, results will be pretty good, most of the time.
p_min = np.array([1E-5,1E-5,1E-7,10.])          # Parameters minima
p_max = np.array([1E-1,1E-2,1E-3,100.])          # Parameters maxima
p_mean = (p_min + p_max)/2.         # Parameters means
p_sigma = (p_max - p_min)/2.        # Parameters standard deviations

# Here a few tweaks that I want to use
a = 0.7                       # Smoothing factor, between 0 and 1
b = 0.14                       # Smoothing power, between ~5 and ~10
c = 0.1                     # Lower limit for the change in parameter estimation
k = 20                        # Max number of iterations
r = 0.1                         # Sample quantile that will define elite

# Performance function
def perf(p):
    R = (data[:,1]-signal(data[:,0],p[0],p[1],p[2],p[3]))**2
    Rmean = np.sum(R)/N
    return Rmean*(1./N)*np.sum((R-Rmean)**2)

# Now, let's estimate the abundances and the spread parameter
new_p_mean,new_p_sigma = n.estimate(perf,p_mean,p_sigma,alpha=a,beta=b,c_limit=c,k_max=k,rho=r)
print 'A_abund = %.3E p/m %.3g' % (new_p_mean[0],new_p_sigma[0])
print 'B_abund = %.3E p/m %.3g' % (new_p_mean[1],new_p_sigma[1])
print 'C_abund = %.3E p/m %.3g' % (new_p_mean[2],new_p_sigma[2])
print 'rot = %.3f p/m %.3f' % (new_p_mean[3],new_p_sigma[3])

estim_y = np.array([signal(xk,new_p_mean[0],new_p_mean[1],new_p_mean[2],new_p_mean[3]) for xk in x])

plt.plot(x,true_y,'r',label='True signal')
plt.plot(x,noisy_y,'.',label='Observed signal')
plt.plot(x,estim_y,'g',label='Fitted signal')
plt.legend()
plt.show()