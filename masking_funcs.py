import numpy as np


def handle_masks(x, y, z=None):
    """take two possibly masked arrays of same shape and return a new, flattened pair of arrays
    that contains only the elements that are unmasked in both of the originals"""

    if z==None:
        
        if x.shape != y.shape:
            raise Exception

        if x.shape == ():
            return x, y

        if not isinstance(x, np.ndarray):
            raise Exception

        if not isinstance(y, np.ndarray):
            raise Exception

        if isinstance(x, np.ma.masked_array) and not isinstance(y, np.ma.masked_array):  ## x masked only
            x_out = x.data[np.logical_not(x.mask)]
            y_out = y[np.logical_not(x.mask)]
        elif not isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array):  ## y masked only
            x_out = x[np.logical_not(y.mask)]
            y_out = y.data[np.logical_not(y.mask)]
        elif isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array):  ## x and y both masked
            x_out = x.data[np.logical_not(y.mask + x.mask)]
            y_out = y.data[np.logical_not(y.mask + x.mask)]
        else:
            x_out = x
            y_out = y

        return x_out, y_out

    else:
        
        if x.shape != y.shape:
            raise Exception

        if x.shape != z.shape:
            raise Exception

        if x.shape == ():
            return x, y, z
        
        if not isinstance(x, np.ndarray):
            raise Exception

        if not isinstance(y, np.ndarray):
            raise Exception

        if not isinstance(z, np.ndarray):
            raise Exception

        if isinstance(x, np.ma.masked_array) and not isinstance(y, np.ma.masked_array) and not isinstance(z, np.ma.masked_array):  ## x masked only
            x_out = x.data[np.logical_not(x.mask)]
            y_out = y[np.logical_not(x.mask)]
            z_out = z[np.logical_not(x.mask)]
        elif not isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array) and not isinstance(z, np.ma.masked_array):  ## y masked only
            x_out = x[np.logical_not(y.mask)]
            y_out = y.data[np.logical_not(y.mask)]
            z_out = z[np.logical_not(y.mask)]
        elif not isinstance(x, np.ma.masked_array) and not isinstance(y, np.ma.masked_array) and isinstance(z, np.ma.masked_array):  ## z masked only
            x_out = x[np.logical_not(z.mask)]
            y_out = y[np.logical_not(z.mask)]
            z_out = z.data[np.logical_not(z.mask)]
        elif isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array) and not isinstance(z, np.ma.masked_array):  ## x and y both masked
            x_out = x.data[np.logical_not(y.mask + x.mask)]
            y_out = y.data[np.logical_not(y.mask + x.mask)]
            z_out = z[np.logical_not(y.mask + x.mask)]
        elif isinstance(x, np.ma.masked_array) and not isinstance(y, np.ma.masked_array) and isinstance(z, np.ma.masked_array):  ## x and z both masked
            x_out = x.data[np.logical_not(x.mask + z.mask)]
            y_out = y[np.logical_not(x.mask + z.mask)]
            z_out = z.data[np.logical_not(x.mask + z.mask)]
        elif not isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array) and isinstance(z, np.ma.masked_array):  ## y and z both masked
            x_out = x[np.logical_not(y.mask + z.mask)]
            y_out = y.data[np.logical_not(y.mask + z.mask)]
            z_out = z.data[np.logical_not(y.mask + z.mask)]
        elif isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array) and isinstance(z, np.ma.masked_array):  ## x, y and z both masked
            x_out = x.data[np.logical_not(y.mask + x.mask + z.mask)]
            y_out = y.data[np.logical_not(y.mask + x.mask + z.mask)]
            z_out = z.data[np.logical_not(y.mask + x.mask + z.mask)]
        else:
            x_out = x
            y_out = y
            z_out = z

        return x_out, y_out



def Nonemask(x):    
    """input list x, and output amsked array, with all values of None in list replaced by masked values"""
    a = np.ma.masked_array(x, dtype=np.float)
    aa = np.ma.masked_invalid(a)
    return aa



