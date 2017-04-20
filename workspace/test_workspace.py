# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:05:49 2017

@author: dromero
"""

import numpy as np
import scipy as sp
import sklearn as sk
import matplotlib.pyplot as plt
import pandas as pd

#%% Create some variables
# This creates a list of values, but it is not a proper matrix/vector
x = np.linspace(0,1,100,endpoint=True)
# this defines the second dimension ( = 1), so that it is indeed a vector
x = x[:,np.newaxis]
y = x**2 + np.random.random(x.shape)

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(x,y)
ypred = reg.predict(x)
rms = np.sqrt(np.mean((y-ypred)**2))



#%% Now we try to save
import save_workspace as sv
sv.save_workspace()