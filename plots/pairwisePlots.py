# -*- coding: utf-8 -*-
"""
Creates a plot matrix, i.e., a 2D array of 2D scatter plots of the columns of a matrix. Provides some options for formatting.
Created on Mon Feb 27 15:35:32 2017

@author: dromero
"""
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt

def label_resize_helper(x,major_size=7,minor_size=5):
    '''
    Helper function to change the size of the axes labels
    '''
    x.tick_params(axis='both',which='major',labelsize=major_size)
    x.tick_params(axis='both',which='minor',labelsize=minor_size)

# Vectorizes the helper function so that it can be applied to a numpy array of axes
label_resize_helper = np.vectorize(label_resize_helper,excluded=['major_size','minor_size'])

def pairwisePlots(data,y_labels=None, feature_names=None, with_legend = False, figure_size = (8,8), diagonal='none'):
    
    # default font/label sizes
    axes_major_label_size = 7
    axes_minor_label_size = 5
    base_font_size = 10
    symbol_size = 8
    base_figure_size = (8,8)
    
    # (naively) re-scale fonts if a different figure size is given
    scale_factor = (figure_size[0] * figure_size[1]) / (base_figure_size[0]*base_figure_size[1])
    scale_factor = np.sqrt(scale_factor)
    # The constants here are fudge factors to get the sizes "right"
    axes_major_label_size = scale_factor/1.5 * axes_major_label_size
    axes_minor_label_size = scale_factor/2 * axes_minor_label_size
    base_font_size = scale_factor/1.5 * base_font_size
    symbol_size = 1+(scale_factor-1)/10
    
    # Number of columns in the data
    nfeatures = data.shape[1]
    
    # Process/prepare data labels and feature names
    if y_labels is None:
        label_set = [0]
    else:
        label_set = np.unique(y_labels)
        num_colors = float(label_set.size)
        colors = np.array([i for i in range(len(label_set))])
        colors = colors/(float(label_set.size)-1)
    
    if feature_names is None:
        feature_names = [r'$x_%d$'%i for i in range(nfeatures)]
    
    # Create (empty) plot matrix
    fig,axes = plt.subplots(nrows=nfeatures, ncols=nfeatures, sharex='col',
                            sharey='none',figsize=figure_size)
    # resizes axes labels
    label_resize_helper(axes,axes_major_label_size,axes_minor_label_size)
    
    # Main plotting loop
    for i in range(nfeatures):
        for j in range(nfeatures):
            ax = axes[i,j]
            if i == j:
                if diagonal == 'hist':
                    ax.hist(data[:,i])
                elif diagonal == 'kde':
                    density = stats.kde.gaussian_kde(data[:,i])
                    xplot = np.linspace(data[:,i].min(), data[:,i].max(), 20)
                    ax.plot(xplot,density(xplot),'k')
                elif diagonal == 'none':
                    ax.text(0.5,0.5,feature_names[i], \
                            transform=ax.transAxes, \
                            horizontalalignment='center', \
                            verticalalignment='center',fontsize=base_font_size)
            else:
                if y_labels is None:
                    ax.scatter(data[:,j], data[:,i],s=symbol_size)
                else:
                    for k in range(len(label_set)):
                        klabel = label_set[k]
                        myColor = plt.cm.rainbow(colors[k])
                        ax.scatter(data[y_labels==klabel,j], data[y_labels==klabel,i],
                               s=symbol_size,c=myColor,label=klabel)
                    if with_legend:
                        ax.legend(label_set,title='Y Labels')
