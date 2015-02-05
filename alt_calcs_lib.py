import pdb
import numpy as np

### functions for calculatin gactive layer thickness from soil temperature data

def calc_alt_1d(tprof, lev):
    zero = 273.15
    nlev = lev.shape[0]
    if tprof[nlev-1] > zero:
        alt = lev[nlev-1]
    else:
        found_thaw = False
        i = 2
        while (not found_thaw) and (i <= nlev):
            if tprof[nlev-i] > zero:
                found_thaw = True
            else:
                i += 1
        if found_thaw:
            z1 = lev[nlev-i]
            z2 = lev[nlev-(i-1)]
            t1 = tprof[nlev-i]
            t2 = tprof[nlev-(i-1)]
            alt = z1 + (t1-zero)*(z2-z1)/(t1-t2)
            x = [t2, zero, t1]
            y = [z2, alt, z1]
            # if (alt >  lev[nlev-1]) or (alt < 0.):
            if (t2 >  zero) or (t1 < zero):
                pdb.set_trace()
            # map_funcs.xyplot(lev, tprof-zero, xrange=[0., alt+1.], overlay_x=[0.,alt], overlay_y = [0.,0.], overlay_linethickness=5.)
            # time.sleep(3)
        else:
            alt = 0.
    return alt

def calc_alt_1d_discr(tprof, lev_interfaces):
    ## instead of linear interpolation, calculate alt as lower boundary of lowermost unfrozen layer, where unfrozen is defined to be T > 0
    zero = 273.15
    nlev = tprof.shape[0]
    if tprof[nlev-1] > zero:
        alt = lev_interfaces[nlev]
    else:
        found_thaw = False
        i = 2
        while (not found_thaw) and (i <= nlev):
            if tprof[nlev-i] > zero:
                found_thaw = True
            else:
                i += 1
        if found_thaw:
            alt = lev_interfaces[nlev-i+1]
        else:
            alt = 0.
    return alt


def altmax_discr(tprof, lev_interface, depth_axis=1, tzero=273.15, nmonth=12, time_axis=0):
    ntim = tprof.shape[time_axis]
    nyears = ntim / nmonth
    dims = tprof.shape[2:]
    IM = dims[1]
    JM = dims[0]
    print(nyears)
    if time_axis == 0 :
        altmax = np.ma.masked_all([nyears,JM,IM])
        for i in range(nyears):
            thawed = tprof[i*12:(i+1)*12,:].max(axis=0) > tzero
            nthawed = thawed.sum(axis=0)
            altmax[i,:] = lev_interface[nthawed]
        return altmax
    else:
        raise NotImplementedError


def altmax_discr_fromtmax(tprof, lev_interface, depth_axis=1, tzero=273.15, time_axis=0):
    nyears = tprof.shape[time_axis]
    dims = tprof.shape[2:]
    IM = dims[1]
    JM = dims[0]
    print(nyears)
    if time_axis == 0 :
        altmax = np.ma.masked_all([nyears,JM,IM])
        for i in range(nyears):
            thawed = tprof[i,:] > tzero
            nthawed = thawed.sum(axis=0)
            altmax[i,:] = lev_interface[nthawed]
        return altmax
    else:
        raise NotImplementedError
