import numpy as np
import Ngl
import pdb
import string
import re

def find_distances(x1, y1, x2, y2):
    """ generalization of Ngl.gc_dist that can take arrays of lat and lon as input and return a ndarray of distances. """
    narrays = 0
    size_output = []
    order_input = []
    if isinstance(x1, np.ndarray):
        IM1 = x1.size
        narrays = narrays+1
        size_output.append(IM1)
        order_input.append(0)
    if isinstance(y1, np.ndarray):
        JM1 = y1.size
        narrays = narrays+1
        size_output.append(JM1)
        order_input.append(1)
    if isinstance(x2, np.ndarray):
        IM2 = x2.size
        narrays = narrays+1
        size_output.append(IM2)
        order_input.append(2)
    if isinstance(y2, np.ndarray):
        JM2 = y2.size
        narrays = narrays+1
        size_output.append(JM2)
        order_input.append(3)
    
    if narrays == 0:
        output = Ngl.gc_dist(x1, y1, x2, y2)
    else:
        output = np.zeros(size_output)
        if narrays == 1:
            if order_input[0] == 0:
                for i in range(0,IM1):
                    output[i] = Ngl.gc_dist(x1[i], y1, x2, y2)
            if order_input[0] == 1:
                for i in range(0,JM1):
                    output[i] = Ngl.gc_dist(x1, y1[i], x2, y2)
            if order_input[0] == 2:
                for i in range(0,IM2):
                    output[i] = Ngl.gc_dist(x1, y1, x2[i], y2)
            if order_input[0] == 3:
                for i in range(0,JM2):
                    output[i] = Ngl.gc_dist(x1, y1, x2, y2[i])
        if narrays == 2:
            if order_input[0] == 0:
                if order_input[1] == 1:
                    for i in range(0,IM1):
                        for j in range(0,JM1):
                            output[i,j] = Ngl.gc_dist(x1[i], y1[j], x2, y2)
                if order_input[1] == 2:
                    for i in range(0,IM1):
                        for j in range(0,IM2):
                            output[i,j] = Ngl.gc_dist(x1[i], y1, x2[j], y2)
                if order_input[1] == 3:
                    for i in range(0,IM1):
                        for j in range(0,JM2):
                            output[i,j] = Ngl.gc_dist(x1[i], y1, x2, y2[j])
            if order_input[0] == 1:
                if order_input[1] == 2:
                    for i in range(0,JM1):
                        for j in range(0,IM2):
                            output[i,j] = Ngl.gc_dist(x1, y1[i], x2[j], y2)
                if order_input[1] == 3:
                    for i in range(0,JM1):
                        for j in range(0,JM2):
                            output[i,j] = Ngl.gc_dist(x1, y1[i], x2, y2[j])
            if order_input[0] == 2:
                if order_input[1] == 3:
                    for i in range(0,IM2):
                        for j in range(0,JM2):
                            output[i,j] = Ngl.gc_dist(x1, y1, x2[i], y2[j])
        if narrays == 3:
            raise NotImplementedError
        if narrays == 4:
            for i in range(0,IM1):
                for j in range(0,JM1):
                    for k in range(0,IM2):
                        for l in range(0,JM2):
                            output[i,j,k,l] = Ngl.gc_dist(x1[i], y1[j], x2[k], y2[l])
                            
    return output

def get_gridcell_edges(lat, lon):
    IM = lon.shape[0]
    JM = lat.shape[0]
    #
    lat_edges = np.zeros(JM+1)
    lon_edges = np.zeros(IM+1)
    #
    lat_edges[0] = max(lat[0] - (lat[1] - lat[0]) / 2., -90.)
    lat_edges[JM] = min(lat[JM-1] + (lat[JM-1] - lat[JM-2]) / 2., 90.)
    for j in range(1,JM):
        lat_edges[j] = (lat[j] + lat[j-1])/2.
    #    
    lon_edges[0] = lon[0] - (lon[1] - lon[0]) / 2.
    lon_edges[IM] = lon[IM-1] + (lon[IM-1] - lon[IM-2]) / 2.
    for i in range(1,IM):
        lon_edges[i] = (lon[i] + lon[i-1])/2.
    #
    return lat_edges, lon_edges
    

def gridcell_areas(lat, lon, mask=None, radius=6372000., lat_edges_in=False, lon_edges_in=False):

    ### assume uniform longitude spacing
    lat_edges, lon_edges = get_gridcell_edges(lat, lon)
    if lon_edges_in:
        IM = lon.shape[0] - 1
        lon_edges = lon[:]
        res_lon = lon_edges[1] - lon_edges[0]
    else:
        IM = lon.shape[0]
        res_lon = lon[1]-lon[0]
        #
    if lat_edges_in:
        JM = lat.shape[0] - 1       
        lat_edges = lat[:] 
    else:
        JM = lat.shape[0]
    southern_edge = np.fmax(lat_edges[0:JM], np.ones(JM)*-89.99)
    northern_edge = np.fmin(lat_edges[1:], np.ones(JM)*89.99)
    #
    area = Ngl.gc_qarea(southern_edge,np.zeros(JM)-res_lon/2.,\
                        northern_edge,np.zeros(JM)-res_lon/2.,\
                        northern_edge,np.zeros(JM)+res_lon/2.,\
                        southern_edge,np.zeros(JM)+res_lon/2.,\
                        radius=radius) ### 1-D array in meters sq.
    area_array = np.array(np.reshape(np.repeat(area,IM), [JM,IM]))
    if not mask==None:
        area_array = np.ma.array(area_array, mask=mask)
    return area_array


def find_closest(lats, lons, lat, lon, mask=None):
    mindist = 1e20
    if mask == None:
        mask = np.zeros([len(lats), len(lons)], dtype=np.bool)
    for i in range(len(lons)):
        for j in range(len(lats)):
            if not mask[j,i]:
                dist = Ngl.gc_dist(lons[i], lats[j], lon, lat)
                if dist < mindist:
                    closest_i = i
                    closest_j = j
                    mindist = dist
    return closest_i, closest_j



def area_integrate(x, lat, lon, minlat=None, maxlat=None, minlon=None, maxlon=None, lataxis=None, lonaxis=None, area=None):
    # wrapper for calling area_average with area_int argment set to true
    x_int = area_average(x, lat, lon, minlat, maxlat, minlon, maxlon, lataxis, lonaxis, area_int=True, area=area)
    #
    return x_int



def area_average(x, lat, lon, minlat=None, maxlat=None, minlon=None, maxlon=None, lataxis=None, lonaxis=None, area_int = False, weights=None, area=None):
    ndims = len(x.shape)
    # adjust lon axis to be ultimate if necessary
    if not (lonaxis == None or lonaxis == ndims-1):
        x = np.rollaxis(x, lonaxis, ndims)
    # adjust lat axis to be penultimate if necessary
    if not (lataxis == None or lonaxis == ndims-2):
        if ( lonaxis == None or lonaxis > lataxis):
            x = np.rollaxis(x, lataxis, ndims-2)
        else:
            x = np.rollaxis(x, lataxis-1, ndims-2)
    #
    x_shape = x.shape
    if type(lat) != type(None) and type(lon) != type(None):
        if x_shape[len(x_shape)-2] == len(lat):
            lat_edges_in = False
        elif x_shape[len(x_shape)-2] == len(lat)-1:
            lat_edges_in = True
        else:
            raise NotImplementedError
        if x_shape[len(x_shape)-1] == len(lon):
            lon_edges_in = False
        elif x_shape[len(x_shape)-1] ==len(lon)-1:
            lon_edges_in = True
        else:
            raise NotImplementedError
    #
    if type(area) == type(None):
        area = gridcell_areas(lat, lon, lon_edges_in=lon_edges_in, lat_edges_in=lat_edges_in)
    #
    if type(x) == type(np.ma.masked_array()):
        # get mask for area mask
        if ndims == 2:
            mask = x.mask
        elif ndims == 3:
            mask = x.mask[0,:]
        elif ndims == 4:
            mask = x.mask[0,0,:]
        elif ndims == 5:
            mask = x.mask[0,0,0,:]
        area = np.ma.masked_array(area, mask=mask)
    #
    if not (minlat==None and maxlat==None and minlon==None and maxlon==None):
        # subset
        latlonlimit_weight_array = get_latlon_limit_weights(lat, lon, minlat=minlat, maxlat=maxlat, minlon=minlon, maxlon=maxlon, lon_edges_in=lon_edges_in, lat_edges_in=lat_edges_in)
        area = area * latlonlimit_weight_array
    #
    if weights != None:
        area = area * weights
    #
    x_ave = (x * area).sum(axis=ndims-1).sum(axis=ndims-2)
    #
    if not area_int:
        x_ave = x_ave / area.sum()
    #
    return x_ave


def get_latlon_limit_weights(lat, lon, minlat=None, maxlat=None, minlon=None, maxlon=None, lat_edges_in=False, lon_edges_in=False):
    """return weights of what fraction of a given gridcell is within the box defined by minlat, maxlat, minlon, maxlon"""

    lat_edges, lon_edges = get_gridcell_edges(lat, lon)
    if lat_edges_in:
        JM = lat.shape[0]-1
        lat_edges = lat
    else:
        JM = lat.shape[0]
    if lon_edges_in:
        IM = lon.shape[0]-1
        lon_edges = lon
    else:
        IM = lon.shape[0]
    latlonlimit_weight_array = np.ones([JM,IM])
    if minlat != None or maxlat != None:
        if minlat == None:
            minlat = lat_edges.min()
        if maxlat == None:
            maxlat = lat_edges.max()
        lat_weight = np.ones(JM)
        for j in range(JM):
            lat_weight[j] = max(0.,-(max(minlat,lat_edges[j]) - min(maxlat,lat_edges[j+1])) / (lat_edges[j+1] - lat_edges[j]))
        latlonlimit_weight_array = (latlonlimit_weight_array.transpose() * lat_weight).transpose()
    if minlon != None or maxlon != None:
        if minlon == None or maxlon == None:
            raise RuntimeError('if minlon or maxlon is set, both must be set')
        lon_weight = np.ones(IM)
        for i in range(IM):
            lon_weight[i] = max(0.,-(max(minlon,lon_edges[i]) - min(maxlon,lon_edges[i+1])) / (lon_edges[i+1] - lon_edges[i]))
        latlonlimit_weight_array = latlonlimit_weight_array * lon_weight
    return latlonlimit_weight_array
        

def parse_latlon_degrees(string_in):
    """input a string with possible degrees, minutes, etc etc; and output decimal value"""
    string_in = string.lstrip(string_in)
    try:
        degrees = float(string_in)
    except:
        try:
            if string_in.find('\xb0') != -1:
                try:
                    degrees = float(string_in[0:string_in.find('\xb0')])
                except:
                    degrees = float(string_in[1:string_in.find('\xb0')])
                minute_string=string_in[string_in.find('\xb0'):]
            elif string_in.find('v') != -1:
                degrees = float(string_in[0:string_in.find('v')])
                minute_string=string_in[string_in.find('v'):]
            elif string_in.find(' ') != -1:
                degrees = float(string_in[0:string_in.find(' ')])
                minute_string=string_in[string_in.find(' '):]
            else:
                raise RuntimeError
        except:
            if string_in.find('o') != -1:
                try:
                    degrees = float(string_in[0:string_in.find('o')])
                except:
                    degrees = float(string_in[1:string_in.find('o')])
                minute_string=string_in[string_in.find('o')+1:]            
            elif string_in.find('???') != -1:
                degrees = float(string_in[0:string_in.find('???')])
                minute_string=string_in[string_in.find('???')+1:]         
            else:
                print(string_in)
                raise RuntimeError       
        found_numeric = False
        while (not found_numeric) and (len(minute_string) >0):
            if re.match('[0-9]', minute_string) == None:
                minute_string = minute_string[1:]
            else:
                found_numeric  = True
        if len(minute_string) >0:
            try:
                minute_float = float(minute_string[0:minute_string.find("'")])
            except:
                minute_float = float(minute_string[0:minute_string.find(" ")])
            #print('+++++++++>'+str(minute_float))
            degrees = degrees + minute_float/60.


    if (string_in.find('S') != -1) or (string_in.find('W') != -1):
        degrees = -degrees
                    
    return degrees


def zonally_repeat(y_array, IM):
    mask = np.repeat(np.expand_dims(y_array, 0), IM, axis=0).transpose()
    return mask
