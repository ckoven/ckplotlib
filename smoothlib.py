import numpy as np
import math as m
import sys
try:
    import xarray as xr
    has_xarray = True
except:
    has_xarray = False


def boxcar_smoother(x, window=1, edge_truncate=None, axis=None, coordinates=None, overlap_dim=1):
    """calculate the running mean (i.e. boxcar smoothing) on a vector of data.
    running_mean(x, window=1, edge_truncate=False, axis=0)"""
    
    ndims = len(x.shape)

    if isinstance(coordinates, np.ndarray):
        output_coords = True
    else:
        output_coords = False

    if isinstance(x, np.ma.core.MaskedArray):
        masked_input =True
        x_masked = np.ma.copy(x)
    else:
        masked_input = False
        x_masked = np.ma.masked_array(np.copy(x))

    if (ndims == 1) :

        if edge_truncate == None:
            ## replace with missing values at edges
                size_out = x.shape[0]
                offset_output = int(window/2)
                offset_input = 0
                win_spread = int((window)/2)
                x_smoothed = np.ma.masked_all(size_out)
                if output_coords:
                    coords_out = coordinates                    
        else:
            if edge_truncate:
                size_out = x.shape[0] - (window - 1)
                offset_output = 0
                offset_input = int(window/2)
                win_spread = int((window)/2)
                x_smoothed = np.zeros(size_out)
                if output_coords:
                    coords_out = coordinates[offset_input:size_out+offset_input]
            else:
                size_out = x.shape[0]
                offset_output = int(window/2)
                offset_input = 0
                win_spread = int((window)/2)
                x_smoothed = np.zeros(size_out)
                x_smoothed[0:offset_output]=x_masked[0:offset_output]
                x_smoothed[size_out-offset_output:size_out] = x_masked[size_out-offset_output:size_out]
                if output_coords:
                    coords_out = coordinates
                    

        if window%2 == 0:
            window_float = np.ones(window+1)
            window_float[0] = 0.5
            window_float[window] = 0.5
        else:
            window_float = np.ones(window)


        for i in range(offset_output,size_out-offset_output):
            x_smoothed[i] = np.sum(x_masked[i+offset_input-win_spread:i+offset_input+win_spread+1]*window_float[:])/np.sum((1.-np.ma.getmaskarray(x_masked[i+offset_input-win_spread:i+offset_input+win_spread+1]))*window_float[:])
            

    elif (ndims == 2):
        if axis != None:
            ### only smooth along one axis
            if edge_truncate:
                size_out = np.array(x.shape)
                size_out[axis] = x.shape[axis] - (window - 1)
                offset_output = 0
                offset_input = int(window/2)
                win_spread = int((window)/2)
                x_smoothed = np.zeros(size_out)
                if output_coords:
                    coords_out = coordinates[offset_input:size_out[axis]+offset_input]
            else:
                size_out = x.shape
                offset_output = int(window/2)
                offset_input = 0
                win_spread = int((window)/2)
                x_smoothed = np.ma.masked_all(size_out)
                if output_coords:
                    coords_out = coordinates

            if window%2 == 0:
                window_float = np.ones(window+1)
                window_float[0] = 0.5
                window_float[window] = 0.5
            else:
                window_float = np.ones(window)

            for i in range(offset_output,size_out[axis]-offset_output):
                if axis == 0:
                    window_sum = ((1.-np.rollaxis(np.ma.getmaskarray(x_masked[i+offset_input-win_spread:i+offset_input+win_spread+1,:]),0,2))*window_float[:]).sum(axis=1)
                    x_smoothed[i,:] = (np.rollaxis(x_masked[i+offset_input-win_spread:i+offset_input+win_spread+1,:],0,2)*window_float[:]).sum(axis=1)/window_sum
                elif axis == 1:
                    window_sum =  ((1.-np.ma.getmaskarray(x_masked[:,i+offset_input-win_spread:i+offset_input+win_spread+1]))*window_float[:]).sum(axis=1)
                    x_smoothed[:,i] = (x_masked[:,i+offset_input-win_spread:i+offset_input+win_spread+1]*window_float[:]).sum(axis=1)/window_sum
        else:
            ### boxcar smooth on both axes
            if edge_truncate:
                raise NotImplementedError
            size_out = x.shape
            x_smoothed = np.ma.masked_all(size_out)
            if window%2 != 0:   ### odd-sized window
                half_window = (window-1)/2
                if overlap_dim != None:   ###data is on cyclic grid, with overlap along one dimension
                    IM = size_out[overlap_dim]
                    JM = size_out[1-overlap_dim]
                    if overlap_dim == 1:
                        x_correctorder = x.copy()
                    else:
                        x_correctorder = x.transpose()                        
                    for i in range(half_window,IM-half_window):
                        for j in range(half_window,JM-half_window):
                            x_smoothed[j,i] = x_correctorder[j-half_window:j+half_window+1,i-half_window:i+half_window+1].mean()
                    for i in range(0,half_window):
                        for j in range(half_window,JM-half_window):
                            x_smoothed[j,i] = np.ma.concatenate([x_correctorder[j-half_window:j+half_window+1,0:i+half_window+1], x_correctorder[j-half_window:j+half_window+1,IM+i-half_window:IM+1]], axis=1).mean()
                            x_smoothed[j,IM-half_window+i] = np.ma.concatenate([x_correctorder[j-half_window:j+half_window+1,IM-2*half_window+i:IM], x_correctorder[j-half_window:j+half_window+1,0:2*half_window-i]], axis=1).mean()
                    if overlap_dim == 1:
                        x_smoothed_correctorder = x_smoothed.copy()
                    else:
                        x_smoothed_correctorder = x_smoothed.transpose()
                    try:
                        x_smoothed_correctorder.mask[1:JM-1,:] = x.mask[1:JM-1,:]
                    except:
                        x_smoothed_correctorder.mask[1:JM-1,:] = x.mask                        
                    return x_smoothed_correctorder
                else:
                    raise NotImplementedError
            else:
                raise NotImplementedError
                    
                
                

    elif (ndims==3):
        if axis == None:
            print('error -- need to specify an axis for 3d smooth call')
            raise NotImplementedError
        else:
            ### only smooth along one axis
            if edge_truncate:
                size_out = np.array(x.shape)
                size_out[axis] = x.shape[axis] - (window - 1)
                offset_output = 0
                offset_input = int(window/2)
                win_spread = int((window)/2)
                x_smoothed = np.zeros(size_out)
                if output_coords:
                    coords_out = coordinates[offset_input:size_out[axis]+offset_input]
            else:
                size_out = x.shape
                offset_output = int(window/2)
                offset_input = 0
                win_spread = int((window)/2)
                x_smoothed = np.ma.masked_all(size_out)
                if output_coords:
                    coords_out = coordinates

            if window%2 == 0:
                window_float = np.ones(window+1)
                window_float[0] = 0.5
                window_float[window] = 0.5
            else:
                window_float = np.ones(window)

            for i in range(offset_output,size_out[axis]-offset_output):
                if axis == 0:
                    x_subset = x_masked[i+offset_input-win_spread:i+offset_input+win_spread+1,:,:]
                    window_sum = ((1.-np.rollaxis(np.ma.getmaskarray(x_subset),0,3))*window_float[:]).sum(axis=2)
                    x_smoothed[i,:,:] = (np.rollaxis(x_subset,0,3)*window_float[:]).sum(axis=2)/window_sum
                elif axis == 1:
                    x_subset = x_masked[:,i+offset_input-win_spread:i+offset_input+win_spread+1,:]
                    window_sum = ((1.-np.rollaxis(np.ma.getmaskarray(x_subset),1,3))*window_float[:]).sum(axis=2)
                    x_smoothed[:,i,:] = (np.rollaxis(x_subset,1,3)*window_float[:]).sum(axis=2)/window_sum
                elif axis == 2:
                    x_subset = x_masked[:,:,i+offset_input-win_spread:i+offset_input+win_spread+1]
                    window_sum = ((1.-np.ma.getmaskarray(x_subset))*window_float[:]).sum(axis=2)
                    x_smoothed[:,:,i] = (x_subset*window_float[:]).sum(axis=2)/window_sum
                else:
                    raise RuntimeError
                    

                            
    else:
        raise NotImplementedError
    #
    if not output_coords:
        return x_smoothed
    else:
        return x_smoothed, coords_out
        

def monthly_to_annual_xarray(array):
    mon_day  = xr.DataArray(np.array([31,28,31,30,31,30,31,31,30,31,30,31]), dims=['month'])
    mon_wgt  = mon_day/mon_day.sum()
    return (array.rolling(time=12, center=False) # rolling
            .construct("month") # construct the array
            .isel(time=slice(11, None, 12)) # slice so that the first element is [1..12], second is [13..24]
            .dot(mon_wgt, dims=["month"]))


def monthly_to_annual(x, axis=0, nmonths=12, calendar="noleap"):
    """convert monthly to annual data. this keeps units constant"""
    ndims = len(x.shape)
    if type(x) == type(np.ma.masked_all([1])):
        masked=True
    else:
        masked=False
    #
    if calendar=='noleap' and nmonths ==12:
        monthlength = np.array([31.,28.,31.,30.,31.,30.,31.,31.,30.,31.,30.,31.])
    elif calendar == None and nmonths == 12:
        monthlength = np.array([30.,30.,30.,30.,30.,30.,30.,30.,30.,30.,30.,30.])
    else:
        raise NotImplementedError
    #
    ntim = x.shape[axis]
    nyears = int(ntim/nmonths)

    if ndims == 1:
        if not masked:
            annual_x = np.zeros(nyears)
        else:
            annual_x = np.ma.masked_all(nyears)
        for i in range(nyears):
            annual_x[i] = (x[i*nmonths:(i+1)*nmonths] * monthlength).sum() / monthlength.sum()
        return annual_x
    elif ndims == 2:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,2)
        n_dim1 = x_rot.shape[0]
        if not masked:
            annual_x = np.zeros([nyears,n_dim1])
        else:
            annual_x = np.ma.masked_all([nyears,n_dim1])
        for i in range(nyears):
            annual_x[i,:] = (x_rot[:,i*nmonths:(i+1)*nmonths] * monthlength).sum(axis=1) / monthlength.sum()
        # rotate time axis back to original position
        if axis == 1:
            annual_x = np.rotate(annual_x,0,2)
        return annual_x
    elif ndims == 3:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,3)
        n_dim1 = x_rot.shape[0]
        n_dim2 = x_rot.shape[1]
        if not masked:
            annual_x = np.zeros([nyears,n_dim1,n_dim2])
        else:
            annual_x = np.ma.masked_all([nyears,n_dim1,n_dim2])            
        for i in range(nyears):
            annual_x[i,:,:] = (x_rot[:,:,i*nmonths:(i+1)*nmonths] * monthlength).sum(axis=2) / monthlength.sum()
        # rotate time axis back to original position
        if axis == 1:
            annual_x = np.rotate(annual_x,0,2)
        elif axis == 2:
            annual_x = np.rotate(annual_x,0,3)
        return annual_x
    elif ndims == 4:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,4)
        n_dim1 = x_rot.shape[0]
        n_dim2 = x_rot.shape[1]
        n_dim3 = x_rot.shape[2]
        if not masked:
            annual_x = np.zeros([nyears,n_dim1,n_dim2,n_dim3])
        else:
            annual_x = np.ma.masked_all([nyears,n_dim1,n_dim2,n_dim3])            
        for i in range(nyears):
            annual_x[i,:,:,:] = (x_rot[:,:,:,i*nmonths:(i+1)*nmonths] * monthlength).sum(axis=3) / monthlength.sum()
        # rotate time axis back to original position
        if axis == 1:
            annual_x = np.rotate(annual_x,0,2)
        elif axis == 2:
            annual_x = np.rotate(annual_x,0,3)
        elif axis == 3:
            annual_x = np.rotate(annual_x,0,4)
        return annual_x
    else:
        raise NotImplementedError
    
        


def meanannualcycle(x, axis=0, nmonths=12):
    ndims = len(x.shape)
    if type(x) == type(np.ma.masked_all([1])):
        masked=True
    else:
        masked=False        
    #
    ntim = x.shape[axis]
    nyears = ntim/nmonths
    #
    if ndims == 1:
        if not masked:
            meanannualcycle_x = np.zeros(nmonths)
        else:
            meanannualcycle_x = np.ma.masked_all(nmonths)
        for i in range(nmonths):
            meanannualcycle_x[i] = x[i::nmonths].mean()
        return meanannualcycle_x
    elif ndims == 2:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,2)
        n_dim1 = x_rot.shape[0]
        if not masked:
            meanannualcycle_x = np.zeros([nmonths,n_dim1])
        else:
            meanannualcycle_x = np.ma.masked_all([nmonths,n_dim1])
        for i in range(nmonths):
            meanannualcycle_x[i,:] = x_rot[:,i::nmonths].mean(axis=1)
        # rotate time axis back to original position
        if axis == 1:
            meanannualcycle_x = np.rotate(meanannualcycle_x,0,2)
        return meanannualcycle_x
    elif ndims == 3:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,3)
        n_dim1 = x_rot.shape[0]
        n_dim2 = x_rot.shape[1]
        if not masked:
            meanannualcycle_x = np.zeros([nmonths,n_dim1,n_dim2])
        else:
            meanannualcycle_x = np.ma.masked_all([nmonths,n_dim1,n_dim2])            
        for i in range(nmonths):
            meanannualcycle_x[i,:,:] = x_rot[:,:,i::nmonths].mean(axis=2)
        # rotate time axis back to original position
        if axis == 1:
            meanannualcycle_x = np.rotate(meanannualcycle_x,0,2)
        elif axis == 2:
            meanannualcycle_x = np.rotate(meanannualcycle_x,0,3)
        return meanannualcycle_x
    else:
        raise NotImplementedError
    
        
    
