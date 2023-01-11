from pylab import imread, imshow
from skimage import transform

def get_slice_coordinates(x, view_side, w):
    """
    This function returns the viewing coordinates along an axis
    given a viewing center, a view width, and an image length 
    along axis.
    
    inputs:
        x -- int viewing center
        view_side -- int view width
        w -- int image length
        
    returns
        x0 -- int
        x1 -- int
    """
    
    if int(0.5*view_side) > x:
        x0 = 0
        x1 = view_side
        
    elif int(0.5*view_side + x) >= w :
        x1 = w
        x0 = w - view_side
        
    else:
        x0 = x - (0.5 * view_side)
        x1 = x0 + view_side

    return int(x0), int(x1)


def flat_zoom_at(image, x, y, linear_zoom):
    """
    This function zooms in on position x, y of image at a 
    magnification of linear_zoom
    
    inputs:
        image -- array
        x -- int viewing center
        y -- int viewing center
        linear_zoom -- int
        
    returns:
        new_image -- array
        x0 -- int view start coordinates
        y0 -- int view start coordinates
    
    """
    h, w = image.shape
    view_side = int( min(w, h) / linear_zoom )
    
    x0, x1 = get_slice_coordinates(x, view_side, w)
    y0, y1 = get_slice_coordinates(y, view_side, h)
        
    new_image = transform.rescale( image[ y0 : y1, x0 : x1], linear_zoom )

    return new_image, x0, y0
    