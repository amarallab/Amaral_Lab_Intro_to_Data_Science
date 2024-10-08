from copy import copy
from matplotlib import gridspec
from numpy import array, arange
from scipy.stats import pearsonr

import matplotlib.pyplot as plt


##########################################################################################
def half_frame(sub, xaxis_label, yaxis_label, font_size = 15, padding = -0.02):
    """Formats frame, axes, and ticks for matplotlib made graphic 
       with half frame.
       
    """

    # Format graph frame and tick marks
    sub.yaxis.set_ticks_position('left')
    sub.xaxis.set_ticks_position('bottom')
    sub.tick_params(axis = 'both', which = 'major', length = 7, width = 1.5, 
                    direction = 'out', pad = 10, labelsize = font_size)
    sub.tick_params(axis = 'both', which = 'minor', length = 5, width = 1.5, 
                    direction = 'out', labelsize = 10)
    for axis in ['bottom','left']:
        sub.spines[axis].set_linewidth(1.5)
        sub.spines[axis].set_position(("axes", padding))
    for axis in ['top','right']:
        sub.spines[axis].set_visible(False)

    # Format axes
    sub.set_xlabel(xaxis_label, fontsize = 1.6 * font_size)
    sub.set_ylabel(yaxis_label, fontsize = 1.6 * font_size)


    
##########################################################################################    
def bottom_frame(sub, xaxis_label, font_size = 15, padding = -0.02):
    """Formats frame, axes, and ticks for matplotlib made graphic with half frame."""

    # Format graph frame and tick marks
    sub.yaxis.set_ticks_position('none')
    sub.yaxis.set_ticklabels([])
    sub.xaxis.set_ticks_position('bottom')
    sub.tick_params(axis = 'x', which = 'major', length = 7, width = 2, 
                    direction = 'out', pad = 10,
                    labelsize = font_size)
    sub.tick_params(axis = 'x', which = 'minor', length = 5, width = 2, 
                    direction = 'out', labelsize = 10)
    for axis in ['bottom']:
        sub.spines[axis].set_linewidth(2)
        sub.spines[axis].set_position(("axes", padding))
    for axis in ['top','right', 'left']:
        sub.spines[axis].set_visible(False)

    # Format axes
    sub.set_xlabel(xaxis_label, fontsize = 1.6 * font_size)


##########################################################################################
def left_frame(axes, xaxis_label, yaxis_label, font_size = 15, padding = -0.02):
    """
    Formats frame, axes, and ticks for matplotlib made graphic with half frame.
    """
    # Format graph frame and tick marks
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('none')
    axes.xaxis.set_ticklabels([])
    axes.tick_params(axis = 'y', which = 'major', length = 7, width = 2, 
                     direction = 'out', pad = 10,
                     labelsize = font_size)
    axes.tick_params(axis = 'y', which = 'minor', length = 0, width = 0, 
                     direction = 'out', labelsize = 0)
    for axis in ['left']:
        axes.spines[axis].set_linewidth(2)
        axes.spines[axis].set_position(("axes", padding))
    for axis in ['bottom','top','right']:
        axes.spines[axis].set_visible(False)

    # Format axes
    axes.set_xlabel(xaxis_label, fontsize = 1.6 * font_size)
    axes.set_ylabel(yaxis_label, fontsize = 1.6 * font_size)
    
    
##########################################################################################
def star(pvalue, thresholds = [0.0001, 0.001, 0.01]):
    """
    Returns number of stars in order to indicate statistical significance

    :param
        pvalue: float
    :return:
        string with 0-3 stars
    """
    if pvalue < thresholds[0]:
        return '***'
    elif pvalue < thresholds[1]:
        return '**'
    elif pvalue < thresholds[2]:
        return '*'

    return ''


##########################################################################################
def place_commas(n):
    """Takes integer and returns string from printing with commas separating factors of 1000
    """
    tmp = str(n)
    n_digits = len(tmp)

    line = ''
    for i in range(n_digits):
        if not (i) % 3 and i != 0:
            line = tmp[-i - 1] + ',' + line
        else:
            line = tmp[-i - 1] + line

    return line


##########################################################################################
def to_tex_scientific(numb, sig_digits = 2):
    """
    Convert a number to classical scientific notation:
    2.5e+6 -> 2.5 x 10^6

    Outputs number as a string of math tex code (e.g., 2.5 \times 10^{6}), meant
    to be used inside a pre-defined math environment.

    numb: Number to convert
    sig_digits: Number of significant digits to use in the mantissa.
    """
    # If the number is too small python does not convert it to scientific
    # notation
    if abs(numb) <= 1e5:
        return str(numb)
#    fmt = "{{:.{}g}}".format(sig_digits)
    
    numb_str = fmt.format(numb)
    mantissa, exponent = numb_str.split("e")

    return f"{mantissa} \times 10^{{{int(exponent)}}}"


##########################################################################################
def get_product_sample_space(outcomes_list):
    """
    Uses recursion to generate a list of outcomes for a complex event
    arising from a list of independent sets of simple events. For example,
    possible outcomes of rolling a die and flipping a coin, or rolling
    several dice.
    
    input:
        outcomes_list -- list of sets with individual outcomes of simple events
        
    outputs:
        events -- list of strings
    """
    internal_list = copy( outcomes_list )
    
    if len(internal_list) == 1:
        outcomes = internal_list.pop()
        events = []
        for value in outcomes:
            events.append( f"_{value}" )
            
#         print('Events', events)
        return sorted(events)
        
    events = []
#     print('--Events', events)    
    outcomes = internal_list.pop()
    
    for event in get_product_sample_space(internal_list):
        for value in outcomes:
            new_event = f"{event}_{value}"
            if new_event[0] == '_':
                new_event = new_event[1:]
            events.append( new_event )
            
    return sorted(events)


##########################################################################################
def playing_with_dice( L, n, die1_throws, die2_throws, my_function, fig_xsize, 
                       my_fontsize ):
    """
    
    """
    
    # Calculate function with dice points
    points, y, y_max, y_min = my_function(die1_throws, die2_throws)
    
    result = pearsonr(points, die1_throws)
    print(f"Spearman's rho is {result[0]:.3f} with an estimated "
          f"significance level of {result[1]:.6f}\n")
    
    # Calculate histogram
    #
    h = [0]*(y_max+1)
    hist_points = array(h)
    hist = array( [h] * (n+1) )

    for i, j in zip(die1_throws, points):
        hist_points[int(j)] += 1
        hist[i, int(j)] += 1

    hist_points = hist_points / L
    hist = hist / L   
    
    # Plot data
    #
    ax = []
    fig = plt.figure( figsize = (fig_xsize, 6.5) )
    gs = gridspec.GridSpec(2, 2, height_ratios = [1, 3], 
                           width_ratios = [6, 1])

    # Marginal probability
    ax.append( fig.add_subplot(gs[0]) )
    half_frame(ax[0], '', 'Probability', font_size = my_fontsize)
    ax[0].bar(y, hist_points, )
    ax[0].set_xlim(y_min - 0.5, y_max + 0.5)
    ax[0].set_xticks(range(y_min, y_max + 1, ))
    ax[0].set_xticklabels([])  
    
    # Probability density
    ax.append( fig.add_subplot(gs[2]) )
    half_frame(ax[1], 'points', '$die_1$', font_size = my_fontsize)
    temp = ax[1].imshow(hist, cmap = plt.cm.cividis, vmin = 0, vmax = 0.05)

    ax[1].set_xlim(y_min - 0.5, y_max + 0.5)
    ax[1].set_ylim(0.5, 6.5)
    ax[1].set_yticks(range(1, 7))

    ax.append( fig.add_subplot(gs[3]) )
    ax[2].set_axis_off()
    cbar = ax[2].figure.colorbar( temp, ax = ax[2], fraction = 1., shrink = 0.8,
                                  ticks = [0, 0.01, 0.02, 0.030, 0.04, 0.05], )
    cbar.ax.set_ylabel( 'Probability', rotation = -90, va = "bottom", 
                        fontsize = 1.2*my_fontsize )

    plt.tight_layout()
    
    return points