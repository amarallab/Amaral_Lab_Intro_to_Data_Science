import matplotlib.pyplot as plt
import pandas as pd

from collections import Counter
from numpy import arange, exp, geomspace, linspace, mean, sqrt, std
from pathlib import Path
from random import sample
from scipy import integrate
from scipy.stats import norm, uniform


###################################################################################
def create_voters(n_voters, real_intentions):
    """
    Given a population size and voter intentions, this functions
    creates a list of voters characterized by their expected 
    candidate selections
    
    inputs:
        n_voters -- int
        real_intentions -- dict with candidate's name as key and 
                           probabilty of getting a vote as value    

    outputs:
        voters -- list of the candidates selected by each voter
    """
    voters = []
    for candidate in real_intentions:
        voters.extend( [candidate] * 
                       int(n_voters * real_intentions[candidate]) )
    
    voters.extend( ['Other'] * (n_voters - len(voters)) )

    if len(voters) != n_voters:
        return None
    
    return voters


###################################################################################
def simulate_poll(voters, poll_size):
    """
    Extracts a sample of size poll_size from the list voters. 
    
    inputs:
        voters -- list of the candidates selected by each voter
        poll_size -- int
        
    returns:
        poll_results -- list of candidates selected by sampled voters 
        counter -- collections.Counter object
    """
    preferences = sample(voters, poll_size)
        
    return preferences, Counter(preferences)
    

###################################################################################
def plot_results( results, x_label, poll_size, half_frame, my_fontsize ):
    """
    Plot results from simulating a poll from a set of voters with the 
    preferences revealed in the election.

    Inputs:
        results -- list of floats with results in each poll
        x_label -- str for graph
        poll_size -- int
        half_frame -- function for plotting
        my_fontize -- int for scaling fonts in plotting

    Returns:
        None
    """
    fig = plt.figure( figsize = (6, 4) )
    ax = fig.add_subplot( 111 )
    half_frame(ax, x_label, 'Frequency', font_size = my_fontsize)
    
    ax.hist( results, bins = arange(0, 40, 1), color = 'gray',
             align = 'mid', rwidth = 0.9 )
    
    ax.set_ylim(0, 30)
    ax.set_xlim(15, 35)
    ax.set_xticks(list(arange(15, 35, 5)))
    
    ax.vlines(mean(results), 0, 30, color = 'k', lw = 2)
    
    ax.text(16, 22, (f"Poll size: {poll_size}\n"
                     f"Mean: {mean(results):>.1f}\n"
                     f"Std. dev.: {std(results):>.1f}"), 
            fontsize = my_fontsize)
    
    plt.tight_layout()
    plt.show()


###################################################################################
def calculate_prob_data(prior, data, p_heads):
    """
    Calculates the probability of observing the data given the prior. 
    Integrates prior distribution multiplied by the probability of observing
    the data given that parameter value using the romb algorithm which 
    requires a list of 1+2^k equally spaced parameter values and the value 
    of the prior at those values
    
    inputs:
        prior -- list of float, values of the prior at different values of parameter
        data -- float, value of observation
        p_heads -- kust of floats, different values of parameter
        
    outputs:
        float, probability of observing the data given the prior
    
    
    """
    integrand = [p*p_theta if data == 1  else (1-p)*p_theta 
                 for p, p_theta in zip(p_heads, prior)]
    
    dx = 1 / len(integrand)
    return integrate.romb(integrand) * dx


###################################################################################
def noisy_regression_data(n, beta_0, beta_1, sigma_x, sigma_y):
    """
    Generates noisy measurement for two variables following
    a linear relationship.

    Inputs:
        n -- int number of points
        beta_0 -- float coefficient order zero
        beta_1 -- float coefficient order one
        sigma_x -- float magnitude of noise for variable x
        sigma_y -- float magnitude of noise for variable y

    Returns:
        array
        array
        dataframe
    """
    # Generate noise terms for y and x variables
    x_noise = norm.rvs(0, sigma_x, n+1)
    y_noise = norm.rvs(0, sigma_y, n+1)

    # Create noisy measurements
    #
    x = linspace(0, 1., n+1)
    y = beta_0 + beta_1 * x + y_noise
    x = x + x_noise

    # Place data into dataframe
    #
    return x, y, pd.DataFrame(list(zip(x, y)), columns=['X', 'Y'])


###################################################################################
def hist_plot( y_max, step, my_fontsize ):
    fig = plt.figure( figsize = (12, 4) )
    ax = fig.add_subplot(111)

    ax.set_xlim(0, 100)
    ax.set_xlabel('Value', fontsize = 1.4* my_fontsize)

    ax.set_xticks(range(0, 101, 10))
    ax.set_xticklabels(range(0, 101, 10), fontsize = my_fontsize)
    
    ax.set_ylim(0, y_max)
    ax.set_ylabel('Frequency', fontsize = 1.4* my_fontsize)

    ax.set_yticks(range(0, y_max, step))
    ax.set_yticklabels(range(0, y_max, step), fontsize = my_fontsize)
    
    return ax

###################################################################################
def box_plot( sizes, my_fontsize ):
    n = len(sizes)
    xticks = arange(0, 101, 10)
    labels = [f"n = {n}" for n in sizes]
    
    fig = plt.figure( figsize = (12, 2*n+1) )
    ax = fig.add_subplot(111)
    
    for axis in ['top','right', 'left']:
        ax.spines[axis].set_visible(False)

    ax.set_xlim(0, 100)
    ax.set_xlabel('Value', fontsize = 1.4* my_fontsize)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, fontsize = my_fontsize)
    ax.vlines( xticks, 0, 1+len(sizes), colors = '0.7', 
               zorder = -10 )
    
    ax.set_ylim(0.5, 0.5+n)
    ax.set_yticks(arange(1, 1+n))
    ax.set_yticklabels(labels, fontsize = my_fontsize)
        
    return ax


###################################################################################
def plot_gaussian( mu, sigma,  half_frame, my_fontsize ):
    x = linspace(norm.ppf(0.0001, mu, sigma), norm.ppf(0.9999, mu, sigma))
    f_x = norm(mu, sigma)
    
    fig = plt.figure( figsize = (7, 4) )
    ax = fig.add_subplot(1,1,1)
    half_frame(ax, "Height", "Probability density", font_size = my_fontsize)
    
    ax.plot(x, f_x.pdf(x), color = "r", linewidth = 2, alpha = 0.9)
    ax.vlines(mu, 0, 0.8, color = 'k', lw = 4, zorder = -10)
    
    ax.set_ylim(0, 1)

    plt.tight_layout()
    plt.show()


###################################################################################
def plot_power_law( half_frame, my_fontsize ):
    data = 1. / uniform.rvs(0, 1, size = 100000)
    x = geomspace(1, 1E6, num = 20)

    fig = plt.figure( figsize = (6, 4.5) )
    ax = fig.add_subplot(1,1,1)
    
    half_frame(ax, "x", "Probability density", font_size = my_fontsize)
    
    ax.hist( data, bins = x , color = 'gray', 
             align = 'mid', rwidth = 0.8, density = True )

    ax.loglog( x, x**(-2) )

    ax.vlines(mean(data), 0, 1, color = 'k', lw = 4, zorder = -10)

    ax.set_ylim(1E-10, 1)
    ax.set_xlim(1, 1E6)
    
    plt.tight_layout()


###################################################################################
def variability_power_law( half_frame, my_fontsize ):
    means = []
    st_devs = []
    for i in range(100):
        data = 1. / uniform.rvs(0, 1, size = 100)
        means.append(mean(data))
        st_devs.append(std(data))
    
    fig = plt.figure( figsize = (10, 3.5) )
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    
    half_frame(ax1, "Sample", "Mean", font_size = my_fontsize)
    ax1.semilogy(means)
    ax1.text( 2, 200, f"Mean varies\nbetween {min(means):.1f} and {max(means):.1f}" )
    ax1.set_xlim(0, 100)
    ax1.set_ylim(1, 400)
    
    half_frame(ax2, "Sample", "Standard\ndeviation", font_size = my_fontsize)
    ax2.semilogy(st_devs)
    ax2.text( 2, 2000, f"Standard deviation varies\nbetween {min(st_devs):.1f} and {max(st_devs):.1f}" )
    ax2.set_xlim(0, 100)
    ax2.set_ylim(1, 4000)
    
    plt.tight_layout()
    plt.show()
    
    
###################################################################################
def variability_gaussian( half_frame, my_fontsize ):
    means = []
    st_devs = []
    for i in range(100):
        data = norm.rvs(500, 50, size = 100)
        means.append(mean(data))
        st_devs.append(std(data))
    
    fig = plt.figure( figsize = (10, 3.5) )
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    
    half_frame(ax1, "Sample", "Mean", font_size = my_fontsize)
    ax1.plot(means)
    ax1.text( 2, 800, f"Mean varies\nbetween {min(means):.1f} and {max(means):.1f}" )
    ax1.set_ylim(0, 1000)
    ax1.set_xlim(0, 100)
    
    half_frame(ax2, "Sample", "Standard\ndeviation", font_size = my_fontsize)
    ax2.plot(st_devs)
    ax2.text( 2, 80, f"Standard deviation varies\nbetween {min(st_devs):.1f} and {max(st_devs):.1f}" )
    ax2.set_ylim(0, 100)
    ax2.set_xlim(0, 100)
    
    plt.tight_layout()
    plt.show()


###################################################################################
def plot_function( half_frame, my_fontsize ):
    s = arange(0.1, 10., 0.1)
    c = arange(0.1, 100., 0.1)
    
    fig = plt.figure( figsize = (10, 4) )
    ax = []
    
    ax.append( fig.add_subplot(121))
    half_frame(ax[-1], 'Intensity, $i$', 'Probability\ndensity', font_size = my_fontsize)
    ax[-1].semilogy(s, exp(-s), 'b-', lw = 2)
    
    ax[-1].set_xlim(0, 10)
    ax[-1].set_ylim(0.00001, 1)
    
    ax.append( fig.add_subplot(122))
    half_frame(ax[-1], 'Cost, $C$', 'Probability\ndensity', font_size = my_fontsize)
    ax[-1].semilogy(c, 1/2*sqrt(1/c)*exp(-sqrt(c)), 'r-', lw = 2)
    
    ax[-1].set_xlim(0, 100)
    ax[-1].set_ylim(0.00001, 1)
    
    plt.tight_layout()
    plt.show()
