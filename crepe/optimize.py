import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt

class normal(object):
    
    # func = function to be fitted
    # perf = performance function
    # p_mean = vector containing the mean of each parameter
    # p_sigma = vector containing the spread of each parameter
    # N = number of samples to be drawn
    
    # Optional:
    # N = number of samples to be drawn. Default = 100
    # rho = sample lower quantile that will define the elite results. Default = 0.1
    # c_limit = lower limit for the relative change in the performance. Default = 0.1
    # k_max = maximum number of iterations. Default = 50
    # alpha = smoothing factor, between 0 and 1. Default = 1.0
    # beta = smoothing level, between ~0.1 and ~0.2 Default = 0.1
    # silent = True or False. Make it True to not print anything on the terminal. Default = False
    
    def estimate(self,perf,p_mean,p_sigma,**kwargs):
        
        # Defaulting the kwargs
        
        if ('N' in kwargs):
            self.N = kwargs['N']
        else:
            self.N = 100
        
        if ('rho' in kwargs):
            self.rho = kwargs['rho']
        else:
            self.rho = 0.1
        
        if ('c_limit' in kwargs):
            self.c_limit = kwargs['c_limit']
        else:
            self.c_limit = 0.1
                    
        if ('k_max' in kwargs):
            self.k_max = kwargs['k_max']
        else:
            self.k_max = 50   
                
        if ('alpha' in kwargs):
            self.alpha = kwargs['alpha']
        else:
            self.alpha = 1.0
                
        if ('beta' in kwargs):
            self.beta = kwargs['beta']
        else:
            self.beta = 0.1
        
        if ('silent' in kwargs):
            self.silent = kwargs['silent']
        else:
            self.silent = False
        
        # Starting a few helpful variables
        self.check = 1.0
        self.q0 = 0.0
        self.k = 0
        self.PN = len(p_mean)   # Number of parameters
        
        # Starting the iteration
        
        while self.check > self.c_limit and self.k < self.k_max:
            
            self.k += 1
            self.p = np.array([[p_mean[i] + p_sigma[i]*np.random.normal() for i in range(self.PN)] for j in range(self.N)])
            self.S = np.array([perf(self.p[j,:]) for j in range(self.N)])
            self.sorted_S = np.sort(self.S)
            self.q = self.sorted_S[np.int(self.N*self.rho)]
            self.check = np.abs(self.q-self.q0)/self.q
            self.q0 = self.q
            self.ind = np.nonzero(self.S < self.q)
            
            self.I = np.zeros(self.N,float)
            for i in range(len(self.ind)):
                self.I[self.ind[i]] = 1.0
                
            # Calculating the new parameters mean vector
            self.p_mean_prev = p_mean
            p_mean = np.array([np.sum(self.I*self.p[:,j])/np.sum(self.I) for j in range(self.PN)])
            p_mean = self.alpha*p_mean + (1.-self.alpha)*self.p_mean_prev
            
            # Calculating the new sigmas
            self.sigma_prev = p_sigma
            p_sigma = np.array([np.sqrt(np.sum(self.I*(p_mean[j]-self.p[:,j])**2)/np.sum(self.I)) for j in range(self.PN)])
            self.alpha_d = self.alpha-self.alpha*(1-self.k**(-1))**(1.0/self.beta)
            p_sigma = self.alpha_d*p_sigma + (1.0-self.alpha_d)*self.sigma_prev
                
        if self.silent == False and self.k == self.k_max:
            print 'Max iteration limit reached.'
        elif self.silent == False and self.k < self.k_max:
            print "CREPE's number of iterations = %i" % self.k
        
        return p_mean,p_sigma