import numpy as np
import Ngl

def linear_interp(data, coord, interp_coord, axis=0):
    """ basic linear interpolation. """
    #
    shape = data.shape
    ndims = len(shape)
    if shape[axis] != len(coord):
        raise exception
    #
    # find levels above and below interpolation level
    reflev_above = np.sum(np.less(coord, interp_coord))-1
    reflev_below = reflev_above+1
    #
    # find weights of these levels
    weight_below = (interp_coord-coord[reflev_above])/(coord[reflev_below]-coord[reflev_above])
    weight_above = 1.-weight_below
    #
    if axis != 0 and ndims > 1:
        # roll axis to first position
        data_roll = np.rollaxis(data,axis,0)
    else:
        data_roll = data
        #
    if ndims > 1:    
        data_reflev = np.squeeze(weight_above*data[reflev_above,:] + weight_below*data[reflev_below,:])
    else:
        data_reflev = np.squeeze(weight_above*data[reflev_above] + weight_below*data[reflev_below])
    #
    return data_reflev


def conservative_interp(data_in, coords_in, coords_out, axis=0):
    """ do a 1-D conservative interpolation; i.e. each value is the mean of the values over the overlapping interval
        assumes both coordinate systems are monotonic positive deltas"""
    shape = data_in.shape
    ndims = len(shape)
    if shape[axis] + 1 != len(coords_in):
        raise exception
    #
    #
    if ndims == 1:
        data_out = np.zeros(len(coords_out)-1)
    elif ndims == 2:
        if axis==0:
            data_out = np.zeros([len(coords_out)-1,shape[1]])
        else:
            raise exception                        
    elif ndims == 3:
        if axis==0:
            data_out = np.zeros([len(coords_out)-1, shape[1], shape[2]])
        else:
            raise exception
    elif ndims == 4:
        if axis==0:
            data_out = np.zeros([len(coords_out)-1, shape[1], shape[2], shape[3]])
        else:
            raise exception
    else:
        raise exception
    #
    #
    for i in range(len(coords_out)-1):
        lower_bound_out = coords_out[i]
        upper_bound_out = coords_out[i+1]
        overlap_interval_total = 0.
        if ndims == 1:
            data_sum_interval = 0.
        elif ndims == 2:
            data_sum_interval = np.zeros(shape[1])
        elif ndims == 3:
            data_sum_interval = np.zeros([shape[1], shape[2]])
        elif ndims == 4:
            data_sum_interval = np.zeros([shape[1], shape[2], shape[3]])
        for j in range(len(coords_in)-1):
            lower_bound_in = coords_in[j]
            upper_bound_in = coords_in[j+1]
            overlap_interval = min(upper_bound_in, upper_bound_out) - max(lower_bound_in,lower_bound_out)
            if overlap_interval > 0.:
                overlap_interval_total = overlap_interval_total + overlap_interval
                if ndims == 1:
                    data_sum_interval = data_sum_interval + overlap_interval * data_in[j]
                elif ndims == 2:
                    data_sum_interval[:] = data_sum_interval[:] + overlap_interval * data_in[j,:]
                elif ndims == 3:
                    data_sum_interval[:,:] = data_sum_interval[:,:] + overlap_interval * data_in[j,:,:]
                elif ndims == 4:
                    data_sum_interval[:,:,:] = data_sum_interval[:,:,:] + overlap_interval * data_in[j,:,:,:]
        if overlap_interval_total < (upper_bound_out - lower_bound_out):
            print('warning: grids do not overlap fully.  assuming value of zero for non-overlapping region. overlap_interval = '+str(overlap_interval_total)+' output grid ingterval = '+str((upper_bound_out - lower_bound_out)))
        if ndims == 1:
            data_out[i] = data_sum_interval / (upper_bound_out - lower_bound_out)
        elif ndims == 2:
            data_out[i,:] = data_sum_interval[:] / (upper_bound_out - lower_bound_out)
        elif ndims == 3:
            data_out[i,:,:] = data_sum_interval[:,:] / (upper_bound_out - lower_bound_out)
        elif ndims == 4:
            data_out[i,:,:,:] = data_sum_interval[:,:,:] / (upper_bound_out - lower_bound_out)
            
    #
    return data_out

def conservative_regrid(data_in, lats_in, lons_in, lats_out, lons_out, centers_out=True, weights_in=None, spherical=True, radius=6372000., dilute_w_masked_data=True, return_frac_input_masked=False):
    #
    """ do a conservative remapping from one 2-d grid to another.  assumes that input coordinate arrays are monotonic increasing (but handles lon jump across meridian) and that lat and lon are second-to last and last dimensions
        possible to mask the input data either by using a masked array or by setting weights array to zero for masked gridcells
        option dilute_w_masked_data means that where the input data is masked, a value of zero is averaged into the output grid, so that global integrals equal.
        setting this false will mean that global integrals do not equal, hoe=wever this could be back-calculated out using the fraction masked if return_frac_input_masked is set to true
        using the weights_in argument will also lead to non-equal global integrals """
    #
    shape = data_in.shape
    ndims = len(shape)
    JM_i = shape[ndims-2]
    IM_i = shape[ndims-1]
    maxlat = 89.9
    if weights_in == None:
        weights_in = np.ones([JM_i,IM_i])
        weights_mask = np.zeros([JM_i,IM_i], dtype=np.bool)
    else:
        weights_mask = weights_in[:] == 0.
    if type(data_in) == np.ma.core.MaskedArray:
        if ndims == 2:
            mask_in = np.logical_or(data_in[:].mask, weights_mask)
        elif ndims == 3:
            mask_in = np.logical_or(data_in[0,:].mask, weights_mask)
        elif ndims == 4:
            mask_in = np.logical_or(data_in[0,0,:].mask, weights_mask)
    else:
        mask_in = np.logical_or(np.zeros([JM_i,IM_i], dtype=np.bool), weights_mask)
    ## check to see if coordinates input are for gridcell centers or edges.  assume that if edges, length of vector will be one longer than length of data
    #
    #
    #
    #
    ####### lats_in
    if len(lats_in) == JM_i:
        if spherical:
            lat_edges_in = np.zeros(JM_i+1)
            lat_edges_in[0] = max(-maxlat, lats_in[0] - 0.5*(lats_in[1] - lats_in[0]))
            lat_edges_in[JM_i] = min(maxlat, lats_in[JM_i-1] + 0.5*(lats_in[JM_i-1] - lats_in[JM_i-2]))
            lat_edges_in[1:JM_i] = (lats_in[0:JM_i-1] + lats_in[1:JM_i])/2.
        else:
            lat_edges_in = np.zeros(JM_i+1)
            lat_edges_in[0] = lats_in[0] - 0.5*(lats_in[1] - lats_in[0])
            lat_edges_in[JM_i] = lats_in[JM_i-1] + 0.5*(lats_in[JM_i-1] - lats_in[JM_i-2])
            lat_edges_in[1:JM_i] = (lats_in[0:JM_i-1] + lats_in[1:JM_i])/2.                
    elif len(lats_in) == JM_i+1:
        lat_edges_in = lats_in
    else:
        raise RuntimeError
    #
    ####### lats_out
    if centers_out:
        JM_o = len(lats_out)
        if spherical:
            lat_edges_out = np.zeros(JM_o+1)
            lat_edges_out[0] = max(-maxlat, lats_out[0] - 0.5*(lats_out[1] - lats_out[0]))
            lat_edges_out[JM_o] = min(maxlat, lats_out[JM_o-1] + 0.5*(lats_out[JM_o-1] - lats_out[JM_o-2]))
            lat_edges_out[1:JM_o] = (lats_out[0:JM_o-1] + lats_out[1:JM_o])/2.
        else:
            lat_edges_out = np.zeros(JM_o+1)
            lat_edges_out[0] = lats_out[0] - 0.5*(lats_out[1] - lats_out[0])
            lat_edges_out[JM_o] = lats_out[JM_o-1] + 0.5*(lats_out[JM_o-1] - lats_out[JM_o-2])
            lat_edges_out[1:JM_o] = (lats_out[0:JM_o-1] + lats_out[1:JM_o])/2.                
    else:
        JM_o = len(lats_out) -1
        lat_edges_out = lats_out
    #
    ####### lons_in
    if len(lons_in) == IM_i:
        lon_edges_in = np.zeros(IM_i+1)
        lon_edges_in[0] = lons_in[0] - 0.5*(lons_in[1] - lons_in[0])
        lon_edges_in[IM_i] = lons_in[IM_i-1] + 0.5*(lons_in[IM_i-1] - lons_in[IM_i-2])
        lon_edges_in[1:IM_i] = (lons_in[0:IM_i-1] + lons_in[1:IM_i])/2.                
    elif len(lons_in) == IM_i+1:
        lon_edges_in = lons_in
    else:
        raise RuntimeError
    #
    ####### lons_out
    if centers_out:
        IM_o = len(lons_out)
        lon_edges_out = np.zeros(IM_o+1)
        lon_edges_out[0] = lons_out[0] - 0.5*(lons_out[1] - lons_out[0])
        lon_edges_out[IM_o] = lons_out[IM_o-1] + 0.5*(lons_out[IM_o-1] - lons_out[IM_o-2])
        lon_edges_out[1:IM_o] = (lons_out[0:IM_o-1] + lons_out[1:IM_o])/2.                
    else:
        IM_o = len(lons_out) -1
        lon_edges_out = lons_out
    #
    #
    #
    ### first define ranges to loop over that map overlapping lat and lons
    lon_looplist = [[]]
    for i in range(IM_o):
        if i > 0:
            lon_looplist.append([])
        ### figure out which lon quadrant to normalize the data to.  if -90<lon<90 then normalize to option 1, otherwise to zero
        if (Ngl.normalize_angle(lon_edges_out[i], 1) < 90.) and (Ngl.normalize_angle(lon_edges_out[i], 1) > -90.):
            lon_sector = 1
        else:
            lon_sector = 0
        min_cell_lon_o = Ngl.normalize_angle(lon_edges_out[i], lon_sector)
        max_cell_lon_o = Ngl.normalize_angle(lon_edges_out[i+1], lon_sector)
        for ii in range(IM_i):
            min_cell_lon_i = Ngl.normalize_angle(lon_edges_in[ii], lon_sector)
            max_cell_lon_i = Ngl.normalize_angle(lon_edges_in[ii+1], lon_sector)
            overlap_interval_lon = min(max_cell_lon_i, max_cell_lon_o) - max(min_cell_lon_i,min_cell_lon_o)
            if overlap_interval_lon > 0.:
                lon_looplist[i].append(ii)
    #
    #
    #
    lat_looplist = [[]]
    for j in range(JM_o):
        if j > 0:
            lat_looplist.append([])
        min_cell_lat_o = lat_edges_out[j]
        max_cell_lat_o = lat_edges_out[j+1]
        for jj in range(JM_i):
            min_cell_lat_i = lat_edges_in[jj]
            max_cell_lat_i = lat_edges_in[jj+1]
            overlap_interval_lat = min(max_cell_lat_i, max_cell_lat_o) - max(min_cell_lat_i,min_cell_lat_o)
            if overlap_interval_lat > 0.:
                lat_looplist[j].append(jj)
    #
    #
    #            
    ### now begin looping over output grid
    total_weights = np.zeros([JM_o,IM_o])
    total_weights_inputmasked = np.zeros([JM_o,IM_o])
    if ndims == 2:
        total_value = np.zeros([JM_o,IM_o])
    elif ndims == 3:
        total_value = np.zeros([shape[0],JM_o,IM_o])
    elif ndims == 4:
        total_value = np.zeros([shape[0],shape[1],JM_o,IM_o])
    else:
        raise RuntimeError
    for i in range(IM_o):
        ### figure out which lon quadrant to normalize the data to.  if -90<lon<90 then normalize to option 1, otherwise to zero
        if (Ngl.normalize_angle(lon_edges_out[i], 1) < 90.) and (Ngl.normalize_angle(lon_edges_out[i], 1) > -90.):
            lon_sector = 1
        else:
            lon_sector = 0
        min_cell_lon_o = Ngl.normalize_angle(lon_edges_out[i], lon_sector)
        max_cell_lon_o = Ngl.normalize_angle(lon_edges_out[i+1], lon_sector)
        for j in range(JM_o):
            min_cell_lat_o = lat_edges_out[j]
            max_cell_lat_o = lat_edges_out[j+1]
            for ii in lon_looplist[i]:
                for jj in lat_looplist[j]:
                    if not(mask_in[jj,ii]) or dilute_w_masked_data:
                        min_cell_lat_i = lat_edges_in[jj]
                        max_cell_lat_i = lat_edges_in[jj+1]
                        min_cell_lon_i = Ngl.normalize_angle(lon_edges_in[ii], lon_sector)
                        max_cell_lon_i = Ngl.normalize_angle(lon_edges_in[ii+1], lon_sector)
                        overlap_interval_lat = min(max_cell_lat_i, max_cell_lat_o) - max(min_cell_lat_i,min_cell_lat_o)
                        overlap_interval_lon = min(max_cell_lon_i, max_cell_lon_o) - max(min_cell_lon_i,min_cell_lon_o)
                        if overlap_interval_lat > 0. and overlap_interval_lon > 0.:
                            fractional_overlap_lat = overlap_interval_lat / (max_cell_lat_i - min_cell_lat_i)
                            fractional_overlap_lon = overlap_interval_lon / (max_cell_lon_i - min_cell_lon_i)
                            fractional_overlap_total = fractional_overlap_lat * fractional_overlap_lon
                            if spherical:
                                weight = fractional_overlap_total * weights_in[jj,ii] * Ngl.gc_qarea(min_cell_lat_i,min_cell_lon_i,max_cell_lat_i,min_cell_lon_i,max_cell_lat_i,max_cell_lon_i,min_cell_lat_i,max_cell_lon_i,radius=radius)
                            else:
                                weight = fractional_overlap_total * weights_in[jj,ii]
                            total_weights[j,i] = total_weights[j,i] + weight
                            if not(mask_in[jj,ii]):
                                total_weights_inputmasked[j,i] = total_weights_inputmasked[j,i] + weight
                                if ndims == 2:
                                    total_value[j,i] = total_value[j,i] + weight * data_in[jj,ii]
                                elif ndims == 3:
                                    total_value[:,j,i] = total_value[:,j,i] + weight * data_in[:,jj,ii]
                                elif ndims == 4:
                                    total_value[:,:,j,i] = total_value[:,:,j,i] + weight * data_in[:,:,jj,ii]
    #
    if ndims > 2:
        total_weights_bc, total_value_bc = np.broadcast_arrays(total_weights, total_value)
        total_weights_inputmasked_bc, total_value_bc = np.broadcast_arrays(total_weights_inputmasked, total_value)
    else:
        total_weights_bc = total_weights
        total_weights_inputmasked_bc = total_weights_inputmasked
    #
    if total_weights_inputmasked.min() > 0.:
        mean_value = total_value[:] / total_weights_bc[:]
        fraction_maskedinput = total_weights_inputmasked[:] / total_weights[:]
    else:
        mean_value = np.ma.masked_array(total_value[:] / total_weights_bc[:], mask=total_weights_inputmasked_bc[:] == 0.)
        fraction_maskedinput = np.ma.masked_array(total_weights_inputmasked[:] / total_weights[:], mask=total_weights_inputmasked[:] == 0.)
    #
    #
    if not return_frac_input_masked:
        return mean_value
    else:
        return mean_value, fraction_maskedinput
                
        
def absdeltalon(lon1, lon2):
    return min(abs(lon1 - lon2), abs(lon1 + 360. - lon2), abs(lon1-lon2-360.))


def natgrid_interp(data_in, lats_in, lons_in, lats_out, lons_out, valid_range=None, wrapping_overlap_interval=10.):
    IM_i = len(lons_in)
    JM_i = len(lats_in)
    IM_o = len(lons_out)
    JM_o = len(lats_out)
    lons_in_interval1 = np.zeros(IM_i)
    lons_in_interval2 = np.zeros(IM_i)
    lons_out_interval1 = np.zeros(IM_o)
    lons_out_interval2 = np.zeros(IM_o)
    for i in range(IM_i):
        lons_in_interval1[i] = Ngl.normalize_angle(lons_in[i], 0)
        lons_in_interval2[i] = Ngl.normalize_angle(lons_in[i], 1)
    for i in range(IM_o):
        lons_out_interval1[i] = Ngl.normalize_angle(lons_out[i], 0)
    if valid_range == None:
        valid_range = [data_in.min(), data_in.max()]
    x_in_interval1 = np.tile(lons_in_interval1,JM_i)
    y_in = np.repeat(lats_in, IM_i)
    z_in = data_in.flatten()
    if lons_in_interval1.max() - lons_in_interval1.min() > 180. and lons_in_interval2.max() - lons_in_interval2.min() > 180.:
        wrap = True
        ## span of lons is greater than 180; assume that it is a global run and therefore needs to be wrapped
        logical_wrapping = np.logical_and(lons_in_interval2[:] > -wrapping_overlap_interval, lons_in_interval2[:] < 0.)
        lons_wrapped = lons_in_interval2[logical_wrapping]
        data_in_wrapped = data_in[:,logical_wrapping]
        IM_wrapped = len(lons_wrapped)
        lons_wrapped_vector = np.tile(lons_wrapped,JM_i)
        lats_wrapped_vector = np.repeat(lats_in, IM_wrapped)
        data_in_wrapped_vector = data_in_wrapped.flatten()
        ### and add them together
        x_in_interval1 = np.concatenate((x_in_interval1, lons_wrapped_vector))
        y_in = np.concatenate((y_in, lats_wrapped_vector))
        z_in = np.concatenate((z_in, data_in_wrapped_vector))
        #
        logical_wrapping = np.logical_and(lons_in_interval2[:] < wrapping_overlap_interval, lons_in_interval2[:] > 0.)
        lons_wrapped = lons_in_interval1[logical_wrapping] + 360.
        data_in_wrapped = data_in[:,logical_wrapping]
        IM_wrapped = len(lons_wrapped)
        lons_wrapped_vector = np.tile(lons_wrapped,JM_i)
        lats_wrapped_vector = np.repeat(lats_in, IM_wrapped)
        data_in_wrapped_vector = data_in_wrapped.flatten()
        ### and add them together
        x_in_interval1 = np.concatenate((x_in_interval1, lons_wrapped_vector))
        y_in = np.concatenate((y_in, lats_wrapped_vector))
        z_in = np.concatenate((z_in, data_in_wrapped_vector))
        # ### reorder output lons
        # lons_out_interval1_unsorted = lons_out_interval1
        # lons_out_interval1 = lons_out_interval1[lons_out_interval1.argsort()]
    output1 = Ngl.natgrid(x_in_interval1, y_in, z_in, lons_out_interval1, lats_out).transpose()
    output_masked = np.ma.masked_array(output1, mask=np.logical_or(output1 < min(valid_range), output1 > max(valid_range)))
    return(output_masked)
    


def bilinear_interp(data_in, lats_in, lons_in, lats_out, lons_out):
    IM_i = len(lons_in)
    JM_i = len(lats_in)
    IM_o = len(lons_out)
    JM_o = len(lats_out)
    #
    #
    ## find four points from old grid that surround each point on new grid
    J_index_below = np.zeros(JM_o, dtype=np.int)
    J_index_above = np.zeros(JM_o, dtype=np.int)
    for j in range(JM_o):
        J_index_below[j] = np.sum(lats_in[:] <= lats_out[j]) - 1
        J_index_above[j] = JM_i - max(np.sum(lats_in[:] >= lats_out[j]), 1)
    #
    I_index_below = np.zeros(IM_o, dtype=np.int)
    I_index_above = np.zeros(IM_o, dtype=np.int)
    for i in range(IM_o):
        found = False
        for ii in range(IM_i):
            if not found:
                if Ngl.normalize_angle(lons_in[ii],0) == Ngl.normalize_angle(lons_out[i],0):
                    I_index_below[i] = ii
                    I_index_above[i] = ii
                    found = True
        for ii in range(IM_i-1):
            if not found:      
                if Ngl.normalize_angle(lons_in[ii],0) < Ngl.normalize_angle(lons_out[i],0) and Ngl.normalize_angle(lons_in[ii+1],0) > Ngl.normalize_angle(lons_out[i],0):
                    I_index_below[i] = ii
                    I_index_above[i] = ii+1
                    found = True
                elif Ngl.normalize_angle(lons_in[ii],1) < Ngl.normalize_angle(lons_out[i],1) and Ngl.normalize_angle(lons_in[ii+1],1) > Ngl.normalize_angle(lons_out[i],1):
                    I_index_below[i] = ii
                    I_index_above[i] = ii+1
                    found = True
        if not found:
            if Ngl.normalize_angle(lons_in[IM_i-1],1) < Ngl.normalize_angle(lons_out[i],1) and Ngl.normalize_angle(lons_in[0],1) > Ngl.normalize_angle(lons_out[i],1):
                    I_index_below[i] = IM_i-1
                    I_index_above[i] = 0
                    found = True
            elif Ngl.normalize_angle(lons_in[IM_i-1],0) < Ngl.normalize_angle(lons_out[i],0) and Ngl.normalize_angle(lons_in[0],0) > Ngl.normalize_angle(lons_out[i],0):
                    I_index_below[i] = IM_i-1
                    I_index_above[i] = 0
                    found = True
        if not found:
            raise RuntimeError
    #
    # print(J_index_below)
    # print(J_index_above)

    # print(I_index_below)
    # print(I_index_above)
    #
    #
    if type(data_in) == np.ma.masked_array:
        masked_in = True
        data_out = np.ma.masked_all([JM_o,IM_o])
    else:
        masked_in = False
        data_out = np.zeros([JM_o,IM_o])
    #
    #
    ### now loop to do the interpolation
    if masked_in:
        for i in range(IM_o):
            for j in range(JM_o):
                if I_index_below[i] != I_index_above[i] and J_index_below[j] != J_index_above[j]:
                    weights = np.ma.masked_all([4])
                    values = np.ma.masked_all([4])
                    weights[0] = absdeltalon(lons_in[I_index_below[i]], lons_out[i]) * abs(lats_in[J_index_below[j]] - lats_out[j])
                    weights[1] = absdeltalon(lons_in[I_index_above[i]], lons_out[i]) * abs(lats_in[J_index_below[j]] - lats_out[j])
                    weights[2] = absdeltalon(lons_in[I_index_below[i]], lons_out[i]) * abs(lats_in[J_index_above[j]] - lats_out[j])
                    weights[3] = absdeltalon(lons_in[I_index_above[i]], lons_out[i]) * abs(lats_in[J_index_above[j]] - lats_out[j])
                    values[0] = data_in[J_index_below[j], I_index_below[i]]
                    values[1] = data_in[J_index_below[j], I_index_above[i]]
                    values[2] = data_in[J_index_above[j], I_index_below[i]]
                    values[3] = data_in[J_index_above[j], I_index_above[i]]
                    weights.mask = values.mask
                    data_out[j,i] = np.sum(weights * values) / np.sum(weights)
                elif I_index_below[i] == I_index_above[i] and J_index_below[j] != J_index_above[j]:
                    weights = np.ma.masked_all([2])
                    values = np.ma.masked_all([2])
                    weights[0] =  abs(lats_in[J_index_below[j]] - lats_out[j])
                    weights[1] =  abs(lats_in[J_index_above[j]] - lats_out[j])
                    values[0] = data_in[J_index_below[j], I_index_below[i]]
                    values[1] = data_in[J_index_above[j], I_index_above[i]]
                    weights.mask = values.mask
                    data_out[j,i] = np.sum(weights * values) / np.sum(weights)
                elif J_index_below[j] == J_index_above[j] and I_index_below[i] != I_index_above[i]:
                    weights = np.ma.masked_all([2])
                    values = np.ma.masked_all([2])
                    weights[0] = absdeltalon(lons_in[I_index_below[i]], lons_out[i])
                    weights[1] = absdeltalon(lons_in[I_index_above[i]], lons_out[i])
                    values[0] = data_in[J_index_below[j], I_index_below[i]]
                    values[1] = data_in[J_index_above[j], I_index_above[i]]
                    weights.mask = values.mask
                    data_out[j,i] = np.sum(weights * values) / np.sum(weights)
                else:
                    data_out[j,i] = data_in[J_index_below[j], I_index_below[i]]
    else:
        for i in range(IM_o):
            for j in range(JM_o):
                if I_index_below[i] != I_index_above[i] and J_index_below[j] != J_index_above[j]:
                    weights = np.zeros([4])
                    values = np.zeros([4])
                    weights[0] = absdeltalon(lons_in[I_index_below[i]], lons_out[i]) * abs(lats_in[J_index_below[j]] - lats_out[j])
                    weights[1] = absdeltalon(lons_in[I_index_above[i]], lons_out[i]) * abs(lats_in[J_index_below[j]] - lats_out[j])
                    weights[2] = absdeltalon(lons_in[I_index_below[i]], lons_out[i]) * abs(lats_in[J_index_above[j]] - lats_out[j])
                    weights[3] = absdeltalon(lons_in[I_index_above[i]], lons_out[i]) * abs(lats_in[J_index_above[j]] - lats_out[j])
                    values[0] = data_in[J_index_below[j], I_index_below[i]]
                    values[1] = data_in[J_index_below[j], I_index_above[i]]
                    values[2] = data_in[J_index_above[j], I_index_below[i]]
                    values[3] = data_in[J_index_above[j], I_index_above[i]]
                    data_out[j,i] = np.sum(weights * values) / np.sum(weights)
                elif I_index_below[i] == I_index_above[i] and J_index_below[j] != J_index_above[j]:
                    weights = np.zeros([2])
                    values = np.zeros([2])
                    weights[0] =  abs(lats_in[J_index_below[j]] - lats_out[j])
                    weights[1] =  abs(lats_in[J_index_above[j]] - lats_out[j])
                    values[0] = data_in[J_index_below[j], I_index_below[i]]
                    values[1] = data_in[J_index_above[j], I_index_above[i]]
                    data_out[j,i] = np.sum(weights * values) / np.sum(weights)
                elif J_index_below[j] == J_index_above[j] and I_index_below[i] != I_index_above[i]:
                    weights = np.zeros([2])
                    values = np.zeros([2])
                    weights[0] = absdeltalon(lons_in[I_index_below[i]], lons_out[i])
                    weights[1] = absdeltalon(lons_in[I_index_above[i]], lons_out[i])
                    values[0] = data_in[J_index_below[j], I_index_below[i]]
                    values[1] = data_in[J_index_above[j], I_index_above[i]]
                    data_out[j,i] = np.sum(weights * values) / np.sum(weights)
                else:
                    data_out[j,i] = data_in[J_index_below[j], I_index_below[i]]
    #
    #
    return(data_out)
    
