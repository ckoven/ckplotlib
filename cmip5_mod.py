

def parse_cmip5_filename(filename):
    n_underscore = filename.count('_')
    args = []
    for i in range(n_underscore):
        args.append(filename[0:filename.find('_')])
        filename = filename[filename.find('_')+1:]
    args.append(int(filename[0:4]))
    args.append(int(filename[4:6]))
    args.append(int(filename[7:11]))
    args.append(int(filename[11:13]))
    # now make into a dict
    if args[1][0] == 'L':
            realm = 'land'
    elif args[1][0] == 'A':
            realm = 'atmos'
    else:
        realm = None
    try:
        institute = cmip5_modelling_center_model_list[args[2]]
    except:
        institute = None
    output = {'variable':args[0], 'freq':args[1], 'model':args[2], 'exp':args[3], 'ensemble':args[4], 'startyear':args[5], 'startmonth':args[6], 'endyear':args[7], 'endmonth':args[8], 'realm':realm, 'institute':institute}
    return output


cmip5_modelling_center_model_list ={
    'ACCESS': 'CAWCR',
    'ACCESS1-0': 'CAWCR',
    'bcc-csm1-1': 'BCC',
    'BNU-ESM': 'GCESS',
    'CanESM2': 'CCCMA',
    'CanCM4': 'CCCMA',
    'CanAM4': 'CCCMA',
    'CCSM4': 'NCAR',
    'CESM1-BGC': 'NSF-DOE-NCAR',
    'CESM1-CAM5': 'NSF-DOE-NCAR',
    'CESM1-CAM5-1-FV2': 'NSF-DOE-NCAR',
    'CESM1-CHEM-CAM5': 'NSF-DOE-NCAR',
    'CESM1-CHEM': 'NSF-DOE-NCAR',
    'CESM1-WACCM': 'NSF-DOE-NCAR',
    'CMCC-CESM': 'CMCC',
    'CMCC-CM': 'CMCC',
    'CMCC-CMS': 'CMCC',
    'CNRM-CM5': 'CNRM-CERFACS',
    'CSIRO-Mk3-6': 'CSIRO-QCCCE',
    'CSIRO-Mk3-6-0': 'CSIRO-QCCCE',
    'EC-EARTH': 'EC-EARTH',
    'FGOALS-G2': '0',
    'FGOALS-gl': '0',
    'FGOALS-S2': '0',
    'FIO-ESM': 'FIO',
    'GEOS-5': 'NASA-GMAO',
    'GFDL-CM2P1': 'GFDL',
    'GFDL-CM3': 'GFDL',
    'GFDL-ESM2G': 'GFDL',
    'GFDL-ESM2M': 'GFDL',
    'GFDL-HIRAM-C180': 'GFDL',
    'GFDL-HIRAM-C360': 'GFDL',
    'GISS-E2-H': 'GISS',
    'GISS-E2-H-CC': 'GISS',
    'GISS-E2-R': 'GISS',
    'GISS-E2-R-CC': 'GISS',
    'GISS-E2CS-H': 'GISS',
    'GISS-E2CS-R': 'GISS',
    'HadCM3': 'MOHC',
    'HadCM3Q': 'MOHC',
    'HadGEM2-AO': 'NMR-KMA',
    'HadGEM2-CC': 'MOHC',
    'HadGEM2-ES': 'MOHC',
    'HiGEM1-2': '0',
    'inmcm4': 'INM',
    'IPSL-CM5A-LR': 'IPSL',
    'IPSL-CM5A-MR': 'IPSL',
    'IPSL-CM5B': 'IPSL',
    'MIROC-ESM': 'MIROC',
    'MIROC-ESM-CHEM': 'MIROC',
    'MIROC4h': 'MIROC',
    'MIROC4m': 'MIROC',
    'MIROC5': 'MIROC',
    'MPI-ESM-HR': 'MPI-M',
    'MPI-ESM-LR': 'MPI-M',
    'MPI-ESM-MR': 'MPI-M',
    'MPI-ESM-P': 'MPI-M',
    'MRI-AGCM3.2H': 'MRI',
    'MRI-AGCM3-2S': 'MRI',
    'MRI-CGCM3': 'MRI',
    'MRI-ESM1': 'MRI',
    'NorESM': 'NCC',
    'NorESM1-M': 'NCC',
    'NorESM1-ME': 'NCC'}
