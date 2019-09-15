### charlie's collection of linear stats functions
import numpy as np
import sys
import pdb
import math as m
    
def linreg( x, y):
    """ calculate a linear regression of y on x, and return the coefficients and the r squared value.
    vector of coefficients, b: b[0] = y-intercept; b[1] = slope, etc."""
    ### some tests
    if not isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        sys.exit('linreg error: x and y must be numpy ndarrays')
    if not x.shape == y.shape:
        sys.exit('linreg error: x and y shapes do not match')

    if isinstance(x, np.ma.masked_array) or isinstance(y, np.ma.masked_array):
        #########  masked arrays
        if isinstance(x, np.ma.masked_array) and isinstance(y, np.ma.masked_array):
            if not np.all(x.mask == y.mask):
                newmask = np.logical_or(x.mask, y.mask)
                x = np.ma.masked_array(x, mask=newmask)
                y = np.ma.masked_array(y, mask=newmask)
        else:
            if isinstance(x, np.ma.masked_array):
                y = np.ma.masked_array(y, mask=x.mask)
            else:
                x = np.ma.masked_array(x, mask=y.mask)
        x_matrix =  np.array([[np.ma.count(x), np.ma.sum(x)],[np.ma.sum(x), np.ma.sum(x*x)]])
        y_matrix =  np.array([[np.ma.sum(y)],[np.ma.sum(x*y)]])

        b = np.dot(np.linalg.inv(x_matrix),y_matrix)
    
        mean_y = np.ma.sum(y)/np.ma.count(x)
        sst = np.ma.sum((y-mean_y)*(y-mean_y))
        y_hat = b[0]+b[1]*x
        ssr = np.ma.sum((y_hat-mean_y)*(y_hat-mean_y))
        r_sq = ssr/sst
        
    else:
        #########  not masked arrays
        x_matrix =  np.array([[np.size(x), np.sum(x)],[np.sum(x), np.sum(x*x)]])
        y_matrix =  np.array([[np.sum(y)],[np.sum(x*y)]])

        b = np.dot(np.linalg.inv(x_matrix),y_matrix)
    
        mean_y = np.sum(y)/np.size(x)
        sst = np.sum((y-mean_y)*(y-mean_y))
        y_hat = b[0]+b[1]*x
        ssr = np.sum((y_hat-mean_y)*(y_hat-mean_y))
        r_sq = ssr/sst

    return b, r_sq


def detrend(y, x=0.):
    ndims_y = np.size(y.shape)
    if ndims_y > 1:
        sys.exit('linreg.detrend error: only working with 1-D data for now')
    y_size = y.shape[0]
    if isinstance(y, np.ma.masked_array):
        if x == 0.:
            x = np.ma.arange(y_size, mask=y.mask)
    else:
        if x == 0.:
            x = np.arange(y_size)
    b, rsq = linreg(x, y)
    y_detrended = y[:] - (b[0]+b[1]*(x[:]-np.mean(x[:])))
    return y_detrended
                          

        
def montecarlotest_linreg(x, y, nsamples=10000, twotailed=True):

    nobs = len(x)

    if isinstance(x, np.ma.masked_array) or isinstance(y, np.ma.masked_array):
        # if one is masked, mask the other
        if not isinstance(x, np.ma.masked_array):
            x_masked = np.ma.masked_array(x)
        else:
            x_masked = x.copy()
        if not isinstance(y, np.ma.masked_array):
            y_masked = np.ma.masked_array(y)
        else:
            y_masked = y.copy()
        # masked arrays,  strip out any value that is masked in either x or y
        x_list = []
        y_list = []
        for i in range(nobs):
            if not (x_masked.mask[i] or y_masked.mask[i]):
                x_list.append(x_masked.data[i])
                y_list.append(y_masked.data[i])
        x_unmasked = np.array(x_list)
        y_unmasked = np.array(y_list)
        nobs = len(x_unmasked)
    else:
        x_unmasked = x.copy()
        y_unmasked = y.copy()
        

    random_slopes = np.zeros(nsamples)
    for i in range(nsamples):
        random_indices1 = np.argsort(np.random.randn(nobs))
        random_indices2 = np.argsort(np.random.randn(nobs))
        x_shuffled = x_unmasked[random_indices1]
        y_shuffled = y_unmasked[random_indices2]
        b_random, r_sq = linreg(x_shuffled, y_shuffled)
        random_slopes[i] = b_random[1]

    b, r_sq = linreg(x_unmasked, y_unmasked)

    slopes_sorted = np.sort(random_slopes[:])
    abs_slopes_sorted = np.sort(np.abs(random_slopes[:]))

    if twotailed:
        n_greater = np.sum(abs(b[1]) > abs_slopes_sorted[:])
        p = float(n_greater) / float(nsamples)
    else:
        if b[1] > 0.:
            n_greater = np.sum(b[1] > slopes_sorted[:])
            p = float(n_greater) / float(nsamples)
        elif b[1] < 0:
            n_less = np.sum(b[1] < slopes_sorted[:])
            p = float(n_less) / float(nsamples)
        else:
            p = 0.0

    return p
        
        

def multivariate_regression(X,y, return_r_sq=False):
    """calculate the multivariate regression of y=Xb; return coefficients.  b = (X'X)^-1 X'y"""
    #
    if type(X) == np.ndarray:
        X_mat = np.matrix(X)
    elif type(X) == np.ma.core.MaskedArray:
        X_mat = np.matrix(X.data)
    else:
        X_mat = X.copy()
    #
    if type(y) == np.ndarray:
        y_mat = np.matrix(y)
    elif type(y) == np.ma.core.MaskedArray:
        y_mat = np.matrix(y.data)
    else:
        y_mat = y.copy()
    #
    # check to make sure shapes are correct.  y should be a vertical vector of length n; X should be n by m.
    #
    shape_y = y_mat.shape
    if (len(shape_y) != 2) or shape_y[1] != 1:
        y_mat = y_mat.transpose()
        shape_y = y_mat.shape
        if (len(shape_y) != 2) or shape_y[1] != 1:
            raise RuntimeError
    #
    shape_X = X_mat.shape
    if (len(shape_X) != 2) or shape_X[0] != shape_y[0]:
        X_mat = X_mat.transpose()
        shape_X = X_mat.shape
        if (len(shape_X) != 2) or shape_X[0] != shape_y[0]:
            raise RuntimeError
    #
    #
    b = (X_mat.transpose() * X_mat).getI() * X_mat.transpose() * y_mat
    #
    Y_pred = X_mat*b
    error = y_mat - Y_pred
    r_sq = Y_pred.var() / y_mat.var()

    if return_r_sq:
        return b, r_sq
    else:
        return b

def regression_maps(x, y):
    """ regress 2 3-d datasets against each other, where the first dimension is the dimension to regress and thes econd two dimensions are, e.g. geographical coordinates"""
    #
    if type(y) == np.ma.core.MaskedArray:
        ymask = np.ma.count(y, axis=0) < 3
    elif type(y) == np.ndarray:
        ymask = np.zeros(y.shape[1:],dtype=np.bool)
    else:
        raise RuntimeError
    if type(x) == np.ma.core.MaskedArray:
        xmask = np.ma.count(x, axis=0) < 3
    elif type(x) == np.ndarray:
        xmask = np.zeros(x.shape[1:],dtype=np.bool)
    else:
        raise RuntimeError
    #
    sharedmask = np.logical_or(xmask,ymask)
    #    
    if y.shape != x.shape:
        raise RuntimeError
    #
    IM = x.shape[1]
    JM = x.shape[2]
    #
    regression_map = np.ma.masked_all([IM,JM])
    for i in range(IM):
        print((str(i) + ' of ' + str(IM)))
        for j in range(JM):
            if not sharedmask[i,j]:
                b, r_sq = linreg(x[:,i,j], y[:,i,j])
                regression_map[i,j] = b[1]
    #
    return regression_map
                
    



def get_phase_amp_annualcycle(x, frequency_in=1./12., axis=0, detrend=None, test=False):
    # take in data and output the amplitude and phase of the annual cycle component
    #
    ndims = len(x.shape)
    if type(x) == type(np.ma.masked_all([1])):
        masked=True
        mask = np.ma.count_masked(x, axis=axis) > 0
    else:
        masked = False
    #
    ntim = x.shape[axis]
    #
    dt = frequency_in
    #
    # check to make sure ntim is an even multiple of 1/frequency_in
    ts_per_year = 1./frequency_in
    if ntim%ts_per_year != 0:
        n_toadd = int(ts_per_year - ntim%ts_per_year)
        len_record = ntim+n_toadd
        ntim=ntim+n_toadd
    else:
        n_toadd=0
        len_record=None
    #
    # calc index of annual cycle
    nyears = int(ntim / ts_per_year)
    #
    # remove mean
    x = x - x.mean(axis=axis)
    #
    if detrend != None:
        raise NotImplementedError
    #
    fftout = np.fft.fft(x[:], n=len_record, axis=axis)
    #fftfreqout = np.fft.fftfreq(ntim, dt)[0:ntim/2]
    #
    annual_fftout = np.squeeze(np.take(fftout, [nyears], axis=axis))
    amp = np.abs(annual_fftout) / ntim
    pha = np.angle(annual_fftout)

    #
    if masked:
        amp = np.ma.masked_array(amp, mask=mask)
        pha = np.ma.masked_array(pha, mask=mask)

    
    return amp, pha
                      
            
        

def quartiles(data):
    if type(data) == np.ma.masked_array:
        data_sort = np.ma.sort(data)[0:data.count()].data
    elif type(data) == np.ndarray:
        data_sort = np.sort(data)
    else:
        data_sort = np.sort(data)
    nobs = len(data_sort)
    if nobs != 1:
        median = np.median(data_sort)
        lower_quartile = np.median(data_sort[0:nobs/2])
        upper_quartile = np.median(data_sort[nobs/2+nobs%2:])
        return [lower_quartile, median, upper_quartile]
    elif nobs == 1:
        median = data_sort[0]
        lower_quartile = data_sort[0]
        upper_quartile = data_sort[0]
        return [lower_quartile, median, upper_quartile]



def ensemble_ave(data_list, time_axis=0):
    """import a list of numpy arrays of the same shape and return the mean of them"""
    n_ens = len(data_list)
    data_out = data_list[0]
    # one possible exception is that the arrays can have different lengths for the time axis.  in this case, pad the input arrays with blank data and calculate means.  assume all arrays start at the same point but may go for different lengths
    ntim = np.ma.masked_all([n_ens], dtype=np.int)
    for i in range(0, n_ens):
        ntim[i] = data_list[i].shape[time_axis]
    if np.all(ntim == ntim[0]):
        for i in range(1, n_ens):
            data_out = data_out + data_list[i]
        data_out = data_out / float(n_ens)
    else:
        max_ntim = ntim.max()
        shape_input_arrays = list(data_list[0].shape)
        shape_input_arrays[time_axis] = max_ntim
        shape_input_arrays.insert(0,n_ens)
        temp_array = np.ma.masked_all(shape_input_arrays)
        for i in range(n_ens):
            if time_axis == 0:
                temp_array[i,0:ntim[i],:] = data_list[i][:]
            elif time_axis == 1:
                temp_array[i,:,0:ntim[i],:] = data_list[i][:]
            elif time_axis == 2:
                temp_array[i,:,:,0:ntim[i],:] = data_list[i][:]
            else:
                raise NotimplementedError
        data_out = temp_array.mean(axis=0)
        
    return data_out


def error_ellipse(x,y, returnmeans=False):
    cov = np.cov(x[:], y[:])
    lambda_, v = np.linalg.eig(cov)
    lambda_ = np.sqrt(lambda_)
    error_ellipse_xaxis = lambda_[0]
    error_ellipse_yaxis = lambda_[1]
    error_ellipse_angle = 90. + np.degrees(np.arctan2(*v[:,0][:]))
    if returnmeans:
        return error_ellipse_xaxis, error_ellipse_yaxis, error_ellipse_angle, x.mean(), y.mean()
    else:
        return error_ellipse_xaxis, error_ellipse_yaxis, error_ellipse_angle
