import numpy as np
import Nio

## written by C. Koven, cdkoven@lbl.gov  ##

def separate_clmhist_bypft(file_in, variable_name=None, IM=None, JM=None, npft=None, verbose = True, pftcoords_file=None):
    """function to separate 1-D or 2_D vector of data into 3-D or 4-D array.  IM is the number of longitude gridpoints, JM is the number of latitude gridpoints, and npft is the number of PFTs.  input argument is the Nio object corresponding to the file you want to open."""

    
    if type(file_in).__name__ != 'NioFile':
        raise RuntimeError

    if pftcoords_file == None:
        pftcoords_file = file_in
    
    pftvars = []
    for variable in file_in.variables:
        dims = file_in.variables[variable].dimensions
        if 'pft' in dims:
            pftvars.append(variable)

    if not variable_name in pftvars:
        if variable_name == None:
            return pftvars
        else:
            print('variable '+variable_name+ ' not in pft variable list.')
            print(pftvars)
            raise RuntimeError
    
    if IM==None:
        IM = np.max(pftcoords_file.variables['pfts1d_ixy'])
    if JM==None:
        JM = np.max(pftcoords_file.variables['pfts1d_jxy'])
    if npft==None:
        npft = np.max(pftcoords_file.variables['pfts1d_itype_veg'])+1 ## zero is valid pft
    

    vardims = list(file_in.variables[variable_name].dimensions)
    ndims_in_wo_pft = len(vardims)-1
    ndims_out = ndims_in_wo_pft+3
    vardims.append('lat')
    vardims.append('lon')
    dims_out_size = []
    for i, dim in enumerate(vardims):
        if dim == 'lat':
            dims_out_size.append(JM)
        elif dim == 'lon':
            dims_out_size.append(IM)
        elif dim == 'pft':
            dims_out_size.append(npft)
            pftdim = i
        else:
            dims_out_size.append(file_in.dimensions[dim])

    badno = file_in.variables[variable_name].attributes['missing_value'][0]

    if ndims_in_wo_pft == 1:
        data_out = np.ma.masked_all(dims_out_size)
        for pft in range(npft):
            print(' running pft '+str(pft) + ' of '+str(npft))
            var_in = file_in.variables[variable_name]
            ### now loop over timesteps
            pftlonindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[0,:] < badno), pftcoords_file.variables['pfts1d_ixy'][:]) -1
            pftlatindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[0,:] < badno), pftcoords_file.variables['pfts1d_jxy'][:]) -1
            for i in range(dims_out_size[0]):
                # if i%10 == 0:
                #     print(' running pft '+str(i) + ' of '+str(dims_out_size[0]))
                varpft = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[0,:] < badno), var_in[i,:])
                varpftindices = pftlonindices + pftlatindices*IM + pft*IM*JM + i*npft*IM*JM
                data_out.flat[varpftindices] = varpft

    elif ndims_in_wo_pft == 0:
        data_out = np.ma.masked_all(dims_out_size)
        for pft in range(npft):
            var_in = file_in.variables[variable_name]
            ### now loop over timesteps
            varpft = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[:] < badno), var_in[:])
            pftlonindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[:] < badno), pftcoords_file.variables['pfts1d_ixy'][:]) -1
            pftlatindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[:] < badno), pftcoords_file.variables['pfts1d_jxy'][:]) -1
            varpftindices = pftlonindices + pftlatindices*IM + pft*IM*JM 
            data_out.flat[varpftindices]= varpft

    else:
        raise NotImplementedError

    return data_out

