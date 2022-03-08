#Created by Ricky Huang
'''Normalizaed response value curve visualization 
   w.r.t. to changing parameters gamma, sigma, and exp'''

import numpy as np
import matplotlib.pyplot as plt
from NrnResponse import *
from NSclasses import *
from UniformGrid import *
import pandas as pd

'''Basic functions for normalization and single-parameter scheme'''
def Normalize(ini, ini_m, gamma = 1, sigma = 0, exp = 1):
    nom = ini**exp
    denom = sigma**exp + ini_m**exp + nom
    return gamma* (nom/denom)

def GammaVar(gamma, N):
    ini, ini_m = GetUniformGrid(N)
    return Normalize(ini, ini_m, gamma, 0, 1)

def SigmaVar(sigma, N):
    ini, ini_m = GetUniformGrid(N)
    return Normalize(ini, ini_m, 1, sigma, 1)

def expVar(exp, N):
    ini, ini_m = GetUniformGrid(N)
    return Normalize(ini, ini_m, 1, 0, exp)

'''DataFrame object set-up'''
def GetDF(N):
    h_gam = 0.5
    h_sig = 1.
    h_exp = 0.1
    ini, ini_m = GetUniformGrid(N)
    # 1 <= gamma <= 3
    gamma = np.arange(1,3+h_gam, h_gam)
    # 0 <= sigma <= 5
    sigma = np.arange(0,5+h_sig, h_sig)
    # 1 <= exp <= 3
    exp = np.arange(1,3+h_exp, h_exp)
    exp = np.round(exp,2)
    res = dict()
    rows = len(exp)*len(sigma)*len(gamma)

    cols = np.zeros((rows, 6))
    cols[:,3] = [ini]*rows
    cols[:,4] = [ini_m]*rows

    for j in range(len(sigma)):
        for k in range(len(exp)):
            for i in range(len(gamma)):
                cols[i*len(sigma)*len(exp)+j*len(exp)+k, 0] = exp[k]
                cols[i*len(sigma)*len(exp)+j*len(exp)+k, 2] = gamma[i]
                cols[i*len(sigma)*len(exp)+j*len(exp)+k, 1] = sigma[j]
                cols[i*len(sigma)*len(exp)+j*len(exp)+k, 5] = Normalize(ini, 
                                        ini_m, gamma[i], sigma[j], exp[k])
            
    res['exp'] = cols[:,0]
    res['sig'] = cols[:,1]
    res['gam'] = cols[:,2]
    res['Tar'] = cols[:,3]
    res['Pool'] = cols[:,4]
    res['Norm'] = cols[:,5]

    df = pd.DataFrame(data = res)
    return df, gamma, sigma, exp

def PlotNormalized(data, g, sigma, exp):
    #plot normalized response value with fixed gamma
    #changing sigma and exponential
    fig = plt.figure(figsize=(15, 5))
    labels = []
    for s in sigma:
        temp = data[(data['sig'] == s) & (data['gam'] == g)]
        plt.plot(temp.exp, temp.Norm)
        labels.append('sigma = {}'.format(s))
        plt.legend(labels)

        plt.xlabel('Exponential Value', fontsize = 12)
        plt.ylabel('Normalized Response', fontsize = 12)
        plt.title('Normalized Response at gamma = {}'.format(g), fontsize = 16)
    plt.show()

df, gamma, sigma, exp = GetDF(10)
for g in gamma:
    PlotNormalized(df, g, sigma, exp)

