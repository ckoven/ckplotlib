import datetime
import time
import numpy as np
import sys

### simple transformation
def day_mo_2_julian(day, month, leap):

    monthlength_leap = np.array([0,31,29,31,30,31,30,31,31,30,31,30,31])
    monthlength_noleap = np.array([0,31,28,31,30,31,30,31,31,30,31,30,31])

    if leap == True:
        monthstart = np.cumsum(monthlength_leap)
    else:
        monthstart = np.cumsum(monthlength_noleap)
        
    julian = monthstart[month-1]+day
    return int(julian)

def julian_2_day_mo(julian, leap):
    ## assume julian = 1 is jan. 1 = month 1, day 1
    monthlength_leap = np.array([0,31,29,31,30,31,30,31,31,30,31,30,31])
    monthlength_noleap = np.array([0,31,28,31,30,31,30,31,31,30,31,30,31])
    month = 1
    done = False
    if leap == True:
        monthlength = monthlength_leap
    else:
        monthlength = monthlength_noleap

    if julian <= monthlength.sum():
        day = julian        
    else:
        raise RuntimeError
    
    while not done:
        if day - monthlength[month] > 0:
            day = day - monthlength[month]
            month = month + 1
        else:
            done = True
    if month > 12:
        print month
        print day
        print julian
        print leap
        sys.exit()
    return day, month



def string2date(datestring):
    format = "%Y-%m-%d"
    timeout = time.strptime(datestring, format)
    dateout = datetime.date(timeout[0], timeout[1], timeout[2])
    return dateout

def string2datetime(datestring):
    format = "%Y-%m-%d %H:%M:%S"
    timeout = time.strptime(datestring, format)
    dateout = datetime.datetime(timeout[0], timeout[1], timeout[2], timeout[3], timeout[4], timeout[5])
    return dateout

def date2decimalyear(datein):
    julian = datein.timetuple()[7]
    year = datein.timetuple()[0]
    if year%4 == 0:
        yeardecimal = year+julian/366.
    else:
        yeardecimal = year+julian/365.
    return yeardecimal

def date2julian(datein):
    if not isinstance(datein, np.ndarray):
        julian = datein.timetuple()[7]
        return julian
    else:
        ndate = datein.size
        julian = np.zeros(ndate)
        for i in range(0,ndate):
            julian[i] = datein[i].timetuple()[7]
        return julian

def coards2year(time_in, timestringIn):
    """ coards2year(time_in, timestringIn)  assume a numpy array for time_in,
    and a string of the sort 'hours since 1950-01-01 00:00:00.0' or the like for timestringIn"""
    import string
    import re
    ntim = time_in.shape[0]
    time_out = np.zeros([ntim])
    stringwords = string.split(timestringIn)
    units = stringwords[0]
    datestartstring = stringwords[2]
    timestartstring = stringwords[3]
    ### strip off any fractions of a second
    timestartstring_split = re.split('\.', timestartstring)
    datetimestartstring = datestartstring + ' ' + timestartstring_split[0]
    datetimestart = string2datetime(datetimestartstring)
    if string.lower(units) == 'hours':
        for i in range(0,ntim):
            thedays = int(time_in[i])/24
            thehours = int(time_in[i])%24
            offsettime = datetime.timedelta(hours=thehours, days=thedays)
            newtime = datetimestart + offsettime
            time_out[i] = date2decimalyear(newtime)
    elif string.lower(units) == 'days':
        for i in range(0,ntim):
            offsettime = datetime.timedelta(days=time_in[i])
            newtime = datetimestart + offsettime
            time_out[i] = date2decimalyear(newtime)
        
    return time_out

def coards2datetimearray(time_in, timestringIn):
    """ coards2year(time_in, timestringIn)  assume a numpy array for time_in,
    and a string of the sort 'hours since 1950-01-01 00:00:00.0' or the like for timestringIn"""
    import string
    import re
    ntim = time_in.shape[0]
    time_out = np.zeros([ntim], dtype=np.dtype(datetime.datetime))
    stringwords = string.split(timestringIn)
    units = stringwords[0]
    datestartstring = stringwords[2]
    timestartstring = stringwords[3]
    ### strip off any fractions of a second
    timestartstring_split = re.split('\.', timestartstring)
    datetimestartstring = datestartstring + ' ' + timestartstring_split[0]
    datetimestart = string2datetime(datetimestartstring)
    if string.lower(units) == 'hours':
        for i in range(0,ntim):
            thedays = int(time_in[i])/24
            thehours = int(time_in[i])%24
            offsettime = datetime.timedelta(hours=thehours, days=thedays)
            time_out[i] = datetimestart + offsettime
    elif string.lower(units) == 'days':
        for i in range(0,ntim):
            offsettime = datetime.timedelta(days=time_in[i])
            time_out[i] = datetimestart + offsettime
    elif string.lower(units) == 'months':
        for i in range(0, ntim):
            monthstart = datetimestart.month
            yearstart = datetimestart.year
            yeardelta = int(time_in[i])/12
            monthdelta = int(time_in[i])%12
            fracmonthdelta = (time_in[i]-int(time_in[i]))
            if monthstart+monthdelta > 12:
                yearend = yearstart+yeardelta+1
                monthend = monthstart + monthdelta - 12
            else:
                yearend = yearstart+yeardelta 
                monthend = monthstart+monthdelta
            time_out[i] = datetimestart
            time_out[i] = time_out[i].replace(year=yearend, month=monthend)
            if time_out[i].year%4 == 0:
                monthlength_array = np.array([0,31,29,31,30,31,30,31,31,30,31,30,31])
                monthlength = monthlength_array[time_out[i].month]
            else:
                monthlength_array = np.array([0,31,28,31,30,31,30,31,31,30,31,30,31])
                monthlength = monthlength_array[time_out[i].month]
            time_out[i] = time_out[i]+ datetime.timedelta(days=monthlength*fracmonthdelta)
                
    return time_out

def yyyymmdd2decimal(date_in, leap=False):
    """change date in YYYYMMDD format to decimal date"""
    monthlength_leap = np.array([0,31,29,31,30,31,30,31,31,30,31,30,31])
    monthlength_noleap = np.array([0,31,28,31,30,31,30,31,31,30,31,30,31])
    year = date_in/10000
    month = (date_in - year*10000 ) / 100
    day = date_in - year*10000 - month*100
    if not leap:
        decimal_date = (monthlength_noleap.cumsum()[month-1] + day-1)/365. + year
    return(decimal_date)
