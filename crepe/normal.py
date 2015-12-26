#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
# This code calculates the best estimation for parameters of a given model.
# These parameters have to be independent of each other, or in other words,
# they follow single-variate Gaussian distributions.
###########################################################################

import numpy as np

class optimize(object):

    """
    Used to do optimization of independent parameters in a multi-parameter
    problem. 
    """
    
    # perf = performance function
    # p_mean = vector containing the mean of each parameter
    # p_sigma = vector containing the spread of each parameter
    
    # Optional:
    # N = number of samples to be drawn. Default = 100
    # rho = sample lower quantile that will define the elite results. 
        # Default = 0.1
    # s_limit = desired lower limit for precision. 
        # Default = 0.01
    # k_max = maximum number of iterations. Default = 50
    # alpha = smoothing factor, between 0 and 1. Default = 1.0
    # beta = smoothing level, between ~0.1 and ~0.2 Default = 0.1
    # silent = True or False. Make it True to not print anything on the 
        # terminal. Default = False
    
    def estimate(self,perf,p_mean,p_sigma,**kwargs):

        """
        Method used to performs the actual estimation of parameters.
        """
        
        # Defaulting the kwargs
        
        if ('N' in kwargs):
            self.N = kwargs['N']
        else:
            self.N = 100
        
        if ('rho' in kwargs):
            self.rho = kwargs['rho']
        else:
            self.rho = 0.1
        
        if ('s_limit' in kwargs):
            self.s_limit = kwargs['s_limit']
        else:
            self.s_limit = 0.01
                    
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
        
        if ('verbose' in kwargs):
            self.verbose = kwargs['verbose']
        else:
            self.verbose = False
            
        if ('c_opt' in kwargs):
            self.c_opt = kwargs['c_opt']
        else:
            self.c_opt = None
        
        # Starting a few helpful variables
        check = 1.0
        q0 = 0.0
        k = 0
        PN = len(p_mean)   # Number of parameters
        
        # Starting the iteration
        
        while check > self.s_limit and k < self.k_max:
            
            k += 1      # iteration counter
            
            # Drawing a sample from a normal distribution
            self.p = np.array([
                [p_mean[i] + p_sigma[i]*np.random.normal() \
                for i in range(PN)] for j in range(self.N)
            ])
            # Following lines:
            # 1) Performance evaluation
            # 2) Sort the performances
            # 3) Get a sample quantile (which will be the elite)
            # 4) Get the indices of the elite sample
            # 5) Get the inverse squared performances (used in calculation)
            self.S = np.array([perf(self.p[j,:]) for j in range(self.N)])
            self.sorted_S = np.sort(self.S)
            self.q = self.sorted_S[np.int(self.N*self.rho)]
            self.ind = np.nonzero(self.S < self.q)
            self.w = self.S**(-2)
            
            
            if self.verbose == True and k > 1:
                #self.sop = p_sigma/p_mean
                print("Iteration %i, sigma/mean = %.3E" % (k,check))
            
            self.I = np.zeros(self.N,float)
            
            for i in range(len(self.ind[0])):
                self.I[self.ind[0][i]] = 1.0
            # Matrix I selects the elite sample (by multiplication)
            
            # Calculating the new parameters mean vector
            self.p_mean_prev = p_mean
            p_mean = np.array([
                np.sum(self.I*self.w*self.p[:,j])/np.sum(self.I*self.w) \
                for j in range(PN)
            ])
            p_mean = self.alpha*p_mean + (1.-self.alpha)*self.p_mean_prev
            
            # Calculating the new sigmas
            self.sigma_prev = p_sigma
            p_sigma = np.array([
                np.sqrt(np.sum(self.I*self.w*(p_mean[j]-self.p[:,j])**2)/np.sum(self.I*self.w)) \
                for j in range(PN)
            ])
            self.alpha_d = self.alpha-self.alpha*(1-k**(-1))**(1.0/self.beta)
            p_sigma = self.alpha_d*p_sigma + (1.0-self.alpha_d)*self.sigma_prev
            if self.c_opt == None:
                check = min(abs(p_sigma/p_mean))
            else:
                check = p_sigma[self.c_opt]/p_mean[self.c_opt]
        
        if self.verbose == True and k == self.k_max:
            print('Max iteration limit reached.')
        elif self.verbose == True and k < self.k_max:
            print("CREPE's number of iterations = %i" % k)
        
        return p_mean,p_sigma
