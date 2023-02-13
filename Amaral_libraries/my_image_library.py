from copy import copy
from numpy import array, mean, uint8
from pylab import imread, imshow
from scipy.stats import linregress, mode, pearsonr
from skimage import transform, img_as_ubyte


##############################################################################
def get_viewing_coordinates( z, viewing_width, l ):
    """
    This function returns the viewing coordinates along an axis
    given a viewing center, a view width, and an image length 
    along axis.
    
    inputs:
        z -- int center coordinate
        viewing_width -- int view width
        l -- int image length
        
    returns
        z0 -- int leftmost coordinate value
        z1 -- int rightmost coordinate value
    """
    
    if int(0.5*viewing_width) > z:
        z0 = 0
        z1 = viewing_width
        
    elif int(0.5*viewing_width + z) >= l :
        z1 = l
        z0 = l - viewing_width
        
    else:
        z0 = z - (0.5 * viewing_width)
        z1 = z0 + viewing_width

    return int(z0), int(z1)


#############################################################################
def grayscale_zoom( image, x, y, zoom_factor ):
    """
    This function zooms in on position x, y of image at a 
    magnification of linear_zoom
    
    inputs:
        image -- array
        x -- int center x coordinate
        y -- int center y coordinate
        zoom_factor -- int
        
    returns:
        zoomed_image -- array
        x0 -- int left corner x coordinate
        y0 -- int left corner y coordinate
    
    """
    h, w = image.shape
    viewing_width = int( min(w, h) / zoom_factor )
    
    x0, x1 = get_viewing_coordinates(x, viewing_width, w)
    y0, y1 = get_viewing_coordinates(y, viewing_width, h)
        
    zoomed_image = img_as_ubyte( transform.rescale( image[ y0 : y1, x0 : x1], 
                                                    zoom_factor ) )
    
    return zoomed_image, x0, y0


#############################################################################
def visualize_tesseract_results( image, results, fig ):
    """
    This function creates a plot for visialization of the ressults from 
    Tesseract's OCR analysis. 
    
    inputs:
        image -- array
        results -- tesseract result object 
        fig -- matplotlib figure object
        
    returns:
    
    """
    ax = fig.add_subplot(111)
    ax.imshow(image, cmap = 'gray')
    
    for i in range(len(results['text'])):
        x = results['left'][i]
        y = results['top'][i]

        w = results['width'][i]
        h = results['height'][i]

        text = results['text'][i]
        conf = int(results['conf'][i])

        if conf > 0: 
            ax.hlines( [y, y+h], x, x+w, color = 'g' )
            ax.vlines( [x, x+w], y, y+h, color = 'g' )
            ax.text( x, y-10, f"{text} ({conf}%)" )
            
            
#############################################################################    
def rescaling_from_OCR_results( x, y, x_values, y_values, results ):
    """
    Calculate data values corresponding to coordinates x (or y) using
    the coordinates in image of a pair of x values (or y values) and the 
    OCR box results returned by Tesseract.
    
    inputs:
        x - int or np.array for x coordinate in image of data point(s)
        y - int or np.array for x coordinate in image of data point(s)
        x_values - values of two x-axis positions ( must have been found by
                                                    Tesseract )
        y_values - values of two y-axis positions ( must have been found by
                                                    Tesseract )
        results - Tesseract image_to_data output results
        
    returns:
       tuple of int or np.array for x value of data point(s) and 
                int or np.array for y value of data point(s)
    """
    # Values need to be sorted for the transformation to work 
    # in this form
    #
    x_values.sort()
    y_values.sort()
    
    # Get x and y fixed points
    #
    i1 = results['text'].index(x_values[0])
    i2 = results['text'].index(x_values[1])

    x1 = int( results['left'][i1] + results['width'][i1] / 2 )
    x2 = int( results['left'][i2] + results['width'][i2] / 2 )
    
    i1 = results['text'].index(y_values[0])
    i2 = results['text'].index(y_values[1])

    y1 = int( results['top'][i1] + results['height'][i1] / 2 )
    y2 = int( results['top'][i2] + results['height'][i2] / 2 )
    
    # Define transformation
    #
    x_scale = (int(x_values[1]) - int(x_values[0])) / (x2 - x1)
    y_scale = (int(y_values[1]) - int(y_values[0])) / (y2 - y1)
    
    x_base = int( x_values[1] )
    y_base = int( y_values[1] )
        
    return ( x_base + (x - x2) * x_scale, 
             y_base + (y - y2) * y_scale )


#############################################################################
def threshold_for_data_extraction( plate, ax1, ax2, coordinates, 
                                   zoom_factor = 4., threshold_for_white = 100 ):
    """
    Transform and RGB image to gray scale, then applies thresholding
    to make B&W version which is returned. 
    Plots grayscale image and zoomed region of B&W image for checking.
    
    inputs:
        plate -- array
        ax1 -- axis object
        ax2 -- axis object
        coordinates -- tuple or list with x and y coordinates to zoom in
        zoom_factor -- float with default value of 4.
        threshold_for_white -- float with default value of 100
        
    outputs:
        plate_for_data -- array
    """
    x, y = coordinates
    plate_g = (256 * plate).astype( uint8 )

    plate_for_data = plate_g > threshold_for_white
    
    ax1.imshow( plate_g, cmap = 'gray', vmin = 0, vmax = 255 )
    
    zoomed_image, x0, y0 = grayscale_zoom(plate_for_data, x, y, zoom_factor)
    ax2.imshow( zoomed_image, cmap = 'gray')
    ax2.plot([zoom_factor * (x-x0)], [zoom_factor * (y-y0)], 'ro')

    return plate_for_data


#############################################################################
def infer_grid_lines( axis, z_min, z_max, w_max, line_threshold, plate ):
    """
    This function takes a selected axis (0 for y and 1 for x), the limits 
    of the relevant coordinate to consider, and the maximum extension along 
    the ortogonal direction, a threshold extension to be considered 
    a grid line, and an array, and return a list of coordinates for the 
    level lines.
    
    inputs:
        axis -- int (0 for y and 1 for x)
        z_min -- int lower limit of region to analyze
        z_max -- int upper limit of region to analyze
        w_max -- int with length of array on ortogonal direction
        line_threshold -- int with number of pixels for coordinate
                            to be considered part of grid line
        plate -- array
        
    returns:
        level_lines -- list of int with coordinates of grid lines
    
    """
    level_lines = []
    levels = []
    level_line_threshold = 10

    print(z_min, z_max)
    if axis == 0:
        for i in range(z_min, z_max):
            j = 0
            while plate[i,j] and j < w_max:
                j += 1

            # Check if this is grid line
            #
            if j > level_line_threshold:
                level_lines.append(i)

            levels.append(j)

    if axis == 1:
        for i in range(z_min, z_max):
            j = w_max
            while plate[j-1, i] and j > 0:
                j -= 1

            # Check if this is grid line
            #
            if w_max - j > line_threshold:
                level_lines.append(i)

            levels.append(w_max - j)
            
    return level_lines, levels


#############################################################################
def cluster_infered_lines( level_lines ):
    """
    Takes list of integers with extracted coordinates of grid lines and  
    returns a float with average of distances between grid lines, list of 
    distances between grid lines, and list of corrected positions of 
    grid lines.

    inputs:
        level_lines -- list of integers (pixel locations)
        
    returns:
        block_delta -- float with average of deltas
        deltas -- list of distances between grid lines
        mapping -- list of floats
    """
    # Peaks indicate center of value or time blocks
    #
    mapping = []

    cluster = [level_lines[0]]
    i = 1
    while i < len(level_lines):
        if level_lines[i] <= cluster[-1] + 5:
            cluster.append(level_lines[i])
        else:
            mapping.append( mean(cluster) )
            cluster = [level_lines[i]]

        i += 1

    mapping.append( mean(cluster) )

    print(f"There are {len(mapping)} level lines:\n   {mapping}")

    # Get distances between peaks in order to do perform scaling
    #
    deltas = []
    for i in range(1, len(mapping)):
        deltas.append( mapping[i] - mapping[i-1] )
    
    block_delta = mean(deltas)
    
    return block_delta, deltas, mapping


############################################################################# 
def correct_column_heights(heights, block_delta, mapping, x_min ):
    """
    This function takes a list of heights of bars, a typical interval 
    between vertical time grids, and a list of coordinates of 
    vertical line grids, and returns a corrected list of column
    heights.
    
    inputs:
        heights -- list of int
        block_delta -- float with average of deltas
        mapping -- list of floats
        x_min -- int lower limit of region to analyze
    
    returns:
        data_values -- values at vertical grid lines
        new_heights -- list of int
    """
    new_heights = copy( heights )

    # This needs commenting!!!
    #
    for x0 in mapping[:]:
        i = int(x0)
        val = []
        for k in range(1-int(block_delta*0.6), int(block_delta*0.6)):
            if heights[i+k-x_min] > 10:
                val.append(heights[i+k-x_min])
                
        step_mode = mode(val)[0][0]

        val_new = []
        i_l = i - int(block_delta*0.6)
        i_r = i_l
        i_l_is_set = False
        for k in range(1-int(block_delta*0.6), int(block_delta*0.6)):
            if ( heights[i+k-x_min] > 0.95 * step_mode and 
                 heights[i+k-x_min] < 1.05 * step_mode ):
                val_new.append(heights[i+k-x_min])     
                if i + k > i_r:
                    i_r = i + k
                i_l_is_set = True
            if not i_l_is_set:
                i_l = i + k

        for k in range(i_l, i_r+1):
            new_heights[k-x_min] = int( mean(val_new) )
            
        # Now that we averaged the heights of the bars inside each segment, 
        # we can easily extract the value at each time segment.
        #
        data_values = []
        for x0 in mapping:
            i = int(x0)
            data_values.append(new_heights[i])

    return data_values, new_heights


############################################################################# 
def rescaling_from_scan_results( axis, z, scale, mapping, z_max = 0 ):
    """
    This function rescales a list or array of values with coordinates 
    according to a linear transformation determined by the values of 
    the scale of the graph and the location of grid lines.
 
    Return an array with data values.
        
    inputs:
        axis -- int (0 for y and 1 for x)
        z -- list or array of coordinates in image of data
        scale -- list of values listed in scale of graph
        mapping -- list of coordinates of grid lines
        z_max -- int with length of array according the direction
                    considered
        
    returns:
        data -- array of floats 
    """
    # Regress mapping on scale
    #
    if axis == 0:
        mapping2 = z_max - array(mapping)
    else:
        mapping2 = array(mapping)
    
    z = array(z)
        
    result = linregress( mapping2, scale )
    data = result.slope * z + result.intercept
    
    return data
    


    
