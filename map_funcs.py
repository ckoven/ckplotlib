import numpy as np
import Ngl
import math
import sys
from copy import deepcopy
import os.path
import subprocess
import inspect
import os
import shlex
try:
    from IPython.display import Image, display
    jupyter_avail = True
except:
    jupyter_avail = False

#print(jupyter_avail)
    
print((Ngl.__version__))

## these are a set of plotting functions using the PyNGL library, developed by C. Koven for own use.

x11_window_list = []  ### this is a running tally of what x11 workstations have been created by this module, for easy clearing of them

### declare a global page width and height (default is square)
# page_width = 8.5
# page_height = 11.
# ### declare a global page width and height (default is square)
page_width = 7.
page_height = 7.

def get_workstation_type(file):
    if type(file) == type(None):
        graphicfiletype = 'x11'
    else:
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension == ".png":
            graphicfiletype = "png"
        else:
            if Ngl.__version__ == "1.3.1":
                graphicfiletype = "newpdf"
            elif Ngl.__version__ == "1.4.0":
                graphicfiletype = "newpdf"    
            elif Ngl.__version__ == "1.5.0" or Ngl.__version__ == "1.5.0-beta":
                graphicfiletype = "pdf"    
            else:
                graphicfiletype = "pdf"
    return graphicfiletype


def clear_all_x11_windows():
    for i in range(len(x11_window_list)):
        temp = x11_window_list.pop()
        Ngl.delete_wks(temp)

def clear_oldest_x11_window():
    try:
        temp = x11_window_list.pop(0)
        Ngl.delete_wks(temp)
    except:
        print('trying to close the oldest x11 window but none are open!')

pngdens = 100

def pdf_to_png(file, density=pngdens):
    ### call some command-line tools to convert a pdf file to a png file.
    ### this assumes that imagemagick tool convert is available, and will use the latex/perl tool pdfcrop if it is available
    ### first crop the pdf file using the perl script pdfcrop (which is in this directory)
    pwdpath = os.getcwd()
    command2stringlist = ['convert','-bordercolor','white','-border','1x1','-trim','-density',str(density),pwdpath+'/'+file+'.pdf',pwdpath+'/'+file+'.png']
    subprocess.check_call(command2stringlist)

def parse_colormap(colormap):
    ### this is to allow the user to specify ether the standard list of PyNGL color tables, or alternately a set of predefined color tables, e.g. the colorbrewer maps, etc.
    ### returns the original colormap name if the colormap is in the standard list, and a set of rgb indices otherwise
    Ngl_colormap_list_old = ['BkBlAqGrYeOrReViWh200','BlAqGrYeOrRe','BlAqGrYeOrReVi200','BlGrYeOrReVi200','BlRe','BlueRedGray','BlueWhiteOrangeRed',
                         'BlueYellowRed','BlWhRe','example','extrema','GrayWhiteGray','GreenYellow','helix1',
                         'hotres','ncview_default','OceanLakeLandSnow','rainbow','rainbow+white+gray','rainbow+white','rainbow+gray',
                         'tbr_240-300','tbr_stdev_0-30','tbr_var_0-500','tbrAvg1','tbrVar1','temp1','thelix',
                         'uniform','wh-bl-gr-ye-re','WhBlGrYeRe','WhBlReWh','WhViBlGrYeOrRe','WhiteBlue','WhiteBlueGreenYellowRed',
                         'WhiteGreen','WhiteYellowOrangeRed','3gauss','3saw','amwg_blueyellowred','BlueDarkRed18','BlueDarkOrange18',
                         'BlueGreen14','Cat12','cosam12','cosam','cyclic','GreenMagenta16','gscyclic',
                         'gsdtol','gsltod','hlu_default','hotcold_18lev','hotcolr_19lev','mch_default','perc2_9lev',
                         'percent_11lev','posneg_1','posneg_2','prcp_2','prcp_3','precip_11lev','precip_diff_12lev',
                         'precip2_15lev','precip2_17lev','precip3_16lev','precip4_11lev','radar','radar_1','rh_19lev',
                         'so4_21','spread_15lev','StepSeq25','sunshine_9lev','sunshine_diff_12lev','temp_diff_18lev','temp_diff_1lev',
                         'topo_15lev','wgne15','hotcolr_19lev','mch_default','perc2_9lev','percent_11lev','precip2_17lev',
                         'precip3_16lev','precip4_11lev','precip4_diff_19lev','precip_diff_12lev','precip_diff_1lev','rh_19lev','spread_15lev',
                         'sunshine_diff_12lev','t2m_29lev','temp_19lev','temp_diff_18lev','topo_15lev','wind_17lev']
    Ngl_colormap_list_new = ['3gauss', '3saw', 'BkBlAqGrYeOrReViWh200', 'BlAqGrYeOrRe', 'BlAqGrYeOrReVi200',
                             'BlGrYeOrReVi200', 'BlRe', 'BlWhRe', 'BlueDarkOrange18', 'BlueDarkRed18',
                             'BlueGreen14', 'BlueRed', 'BlueRedGray', 'BlueWhiteOrangeRed', 'BlueYellowRed',
                             'BrownBlue12', 'CBR_coldhot', 'CBR_drywet', 'CBR_set3', 'CBR_wet',
                             'Cat12', 'GHRSST_anomaly', 'GMT_cool', 'GMT_copper', 'GMT_drywet',
                             'GMT_gebco', 'GMT_globe', 'GMT_gray', 'GMT_haxby', 'GMT_hot',
                             'GMT_jet', 'GMT_nighttime', 'GMT_no_green', 'GMT_ocean', 'GMT_paired',
                             'GMT_panoply', 'GMT_polar', 'GMT_red2green', 'GMT_relief', 'GMT_relief_oceanonly',
                             'GMT_seis', 'GMT_split', 'GMT_topo', 'GMT_wysiwyg', 'GMT_wysiwygcont',
                             'GrayWhiteGray', 'GreenMagenta16', 'GreenYellow', 'MPL_Accent', 'MPL_Blues',
                             'MPL_BrBG', 'MPL_BuGn', 'MPL_BuPu', 'MPL_Dark2', 'MPL_GnBu',
                             'MPL_Greens', 'MPL_Greys', 'MPL_OrRd', 'MPL_Oranges', 'MPL_PRGn',
                             'MPL_Paired', 'MPL_Pastel1', 'MPL_Pastel2', 'MPL_PiYG', 'MPL_PuBu',
                             'MPL_PuBuGn', 'MPL_PuOr', 'MPL_PuRd', 'MPL_Purples', 'MPL_RdBu',
                             'MPL_RdGy', 'MPL_RdPu', 'MPL_RdYlBu', 'MPL_RdYlGn', 'MPL_Reds',
                             'MPL_Set1', 'MPL_Set2', 'MPL_Set3', 'MPL_Spectral', 'MPL_StepSeq',
                             'MPL_YlGn', 'MPL_YlGnBu', 'MPL_YlOrBr', 'MPL_YlOrRd', 'MPL_afmhot',
                             'MPL_autumn', 'MPL_bone', 'MPL_brg', 'MPL_bwr', 'MPL_cool',
                             'MPL_coolwarm', 'MPL_copper', 'MPL_cubehelix', 'MPL_flag', 'MPL_gist_earth',
                             'MPL_gist_gray', 'MPL_gist_heat', 'MPL_gist_ncar', 'MPL_gist_rainbow', 'MPL_gist_stern',
                             'MPL_gist_yarg', 'MPL_gnuplot', 'MPL_gnuplot2', 'MPL_hot', 'MPL_hsv',
                             'MPL_jet', 'MPL_ocean', 'MPL_pink', 'MPL_prism', 'MPL_rainbow',
                             'MPL_s3pcpn', 'MPL_s3pcpn_l', 'MPL_seismic', 'MPL_spring', 'MPL_sstanom',
                             'MPL_summer', 'MPL_terrain', 'MPL_winter', 'NCV_banded', 'NCV_blu_red',
                             'NCV_blue_red', 'NCV_bright', 'NCV_gebco', 'NCV_jaisnd', 'NCV_jet',
                             'NCV_manga', 'NCV_rainbow2', 'NCV_roullet', 'OceanLakeLandSnow', 'SVG_Gallet13',
                             'SVG_Lindaa06', 'SVG_Lindaa07', 'SVG_bhw3_22', 'SVG_es_landscape_79', 'SVG_feb_sunrise',
                             'SVG_foggy_sunrise', 'SVG_fs2006', 'StepSeq25', 'ViBlGrWhYeOrRe', 'WhBlGrYeRe',
                             'WhBlReWh', 'WhViBlGrYeOrRe', 'WhViBlGrYeOrReWh', 'WhiteBlue', 'WhiteBlueGreenYellowRed',
                             'WhiteGreen', 'WhiteYellowOrangeRed', 'amwg', 'amwg256', 'amwg_blueyellowred',
                             'cb_9step', 'cb_rainbow', 'cb_rainbow_inv', 'circular_0', 'circular_1',
                             'circular_2', 'cmp_b2r', 'cmp_flux', 'cmp_haxby', 'cosam',
                             'cosam12', 'cyclic', 'default', 'detail', 'example',
                             'extrema', 'grads_default', 'grads_rainbow', 'gscyclic', 'gsdtol',
                             'gsltod', 'gui_default', 'helix', 'helix1', 'hlu_default',
                             'hotcold_18lev', 'hotcolr_19lev', 'hotres', 'lithology', 'matlab_hot',
                             'matlab_hsv', 'matlab_jet', 'matlab_lines', 'mch_default', 'ncl_default',
                             'ncview_default', 'nice_gfdl', 'nrl_sirkes', 'nrl_sirkes_nowhite', 'perc2_9lev',
                             'percent_11lev', 'posneg_1', 'posneg_2', 'prcp_1', 'prcp_2',
                             'prcp_3', 'precip2_15lev', 'precip2_17lev', 'precip3_16lev', 'precip4_11lev',
                             'precip4_diff_19lev', 'precip_11lev', 'precip_diff_12lev', 'precip_diff_1lev', 'psgcap',
                             'radar', 'radar_1', 'rainbow', 'rainbow+gray', 'rainbow+white',
                             'rainbow+white+gray', 'rh_19lev', 'seaice_1', 'seaice_2', 'so4_21',
                             'so4_23', 'spread_15lev', 'sunshine_9lev', 'sunshine_diff_12lev', 't2m_29lev',
                             'tbrAvg1', 'tbrStd1', 'tbrVar1', 'tbr_240-300', 'tbr_stdev_0-30',
                             'tbr_var_0-500', 'temp1', 'temp_19lev', 'temp_diff_18lev', 'temp_diff_1lev',
                             'testcmap', 'thelix', 'topo_15lev', 'uniform', 'wgne15',
                             'wh-bl-gr-ye-re', 'wind_17lev', 'wxpEnIR']
    if colormap in Ngl_colormap_list_new or type(colormap) == type([]):
        if type(colormap) == type([]):
            print(colormap)
        return colormap
    else:
        # if colormap == 'cb_GnBu':
        #     colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [247,252,240], [224,243,219], [204,235,197], [168,221,181], [123,204,196], [78,179,211], [43,140,190], [8,104,172], [8,64,129]])/256.
        if colormap == 'cb_YlGnBu':
            colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [255,255,217], [237,248,177], [199,233,180], [127,205,187], [65,182,196], [29,145,192], [34,94,168], [37,52,148], [8,29,88]])/256.
        elif colormap == 'cb_YlGnBu2':
            colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [255,255,217], [246,252,197], [237,248,177], [218,240,179], [199,233,180], [163,219,183], [127,205,187], [96,193,192], [65,182,196], [47,164,194], [29,145,192], [31,120,180], [34,94,168], [35,73,158], [37,52,148], [22,41,118], [8,29,88]])/256.
        elif colormap == 'cb_PuRd':
            colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [247,244,249], [231,225,239], [212,185,218], [201,148,199], [223,101,176], [231,41,138], [206,18,86], [152,0,67], [103,0,31]])/256.
        elif colormap == 'cb_RdPu':
            colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [247,244,249], [255,247,243], [253,224,221], [252,197,192], [250,159,181], [247,104,161], [221,52,151], [174,1,126], [122,1,119], [73,0,106]])/256.
        elif colormap == 'cb_YlGn':
            colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [255,255,229], [247,252,185], [217,240,163], [173,221,142], [120,198,121], [65,171,93], [35,132,67], [0,104,55], [0,69,41]])/256.
        elif colormap == 'cb_YlOrBr':
            colorvalues = np.array([[256,256,256], [0,0,0], [256,256,256], [255,255,229], [255,247,188], [254,227,145], [254,196,79], [254,153,41], [236,112,20], [204,76,2], [153,52,4], [102,37,6]])/256.
        elif colormap == 'cb_PiYG':
            colorvalues = np.array([[256,256,256], [0,0,0], [142,1,82], [197,27,125], [222,119,174], [241,182,218], [253,224,239], [247,247,247], [230,245,208], [184,225,134], [127,188,65], [77,146,33], [39,100,25]])/256.
        elif colormap == 'cb_BrBG':
            colorvalues = np.array([[256,256,256], [0,0,0], [84,48,5], [140,81,10], [191,129,45], [223,194,125], [246,232,195], [245,245,245], [199,234,229], [128,205,193], [53,151,143], [1,102,94], [0,60,48]])/256.
        elif colormap == 'cb_Paired':
            colorvalues = np.array([[256,256,256], [0,0,0], [166,206,227], [31,120,180], [178,223,138], [51,160,44], [251,154,153], [227,26,28], [253,191,111], [255,127,0], [202,178,214], [106,61,154], [255,255,153], [177,89,40]])/256.
        elif colormap == 'cb_Set1':
            colorvalues = np.array([[256,256,256], [0,0,0], [228,26,28], [55,126,184], [77,175,74], [152,78,163], [255,127,0], [255,255,51], [166,86,40], [247,129,191], [153,153,153]])/256.
        elif colormap == 'cb_Set3':
            colorvalues = np.array([[256,256,256], [0,0,0], [141,211,199], [255,255,179], [190,186,218], [251,128,114], [128,177,211], [253,180,98], [179,222,105], [252,205,229], [217,217,217]])/256.
        elif colormap == 'cb_rainbow':
            colorvalues = np.array([[256,256,256], [0,0,0], [77, 0, 77], [76, 1, 79], [75, 2, 82], [74, 3, 84], [73, 3, 87], [72, 4, 89], [71, 6, 92], [70, 7, 94], [68, 8, 97], [67, 9, 99], [65, 10, 102],
                                    [64, 12, 105], [62, 13, 107], [60, 14, 110], [58, 16, 112], [56, 17, 115], [54, 19, 117], [52, 20, 120], [50, 22, 122], [48, 24, 125], [46, 25, 128], [44, 27, 130],
                                    [42, 29, 133], [40, 31, 135], [38, 33, 138], [35, 35, 140], [37, 41, 143], [39, 47, 145], [41, 54, 148], [44, 60, 150], [46, 67, 153], [48, 74, 156], [51, 80, 158],
                                    [53, 87, 161], [55, 94, 163], [58, 101, 166], [61, 108, 168], [63, 114, 171], [66, 121, 173], [69, 128, 176], [71, 135, 179], [74, 142, 181], [77, 149, 184], [80, 156, 186],
                                    [83, 163, 189], [86, 170, 191], [89, 176, 194], [92, 183, 196], [95, 190, 199], [99, 197, 201], [102, 203, 204], [105, 207, 203], [109, 209, 202], [112, 212, 200], [116, 214, 199],
                                    [119, 217, 198], [123, 219, 197], [126, 222, 196], [130, 224, 195], [134, 227, 194], [138, 230, 193], [142, 232, 193], [145, 235, 192], [149, 237, 192], [153, 240, 192], [157, 242, 192],
                                    [162, 245, 192], [166, 247, 192], [170, 250, 193], [174, 252, 194], [179, 255, 194], [174, 252, 187], [170, 250, 180], [166, 247, 173], [162, 245, 166], [157, 242, 158], [156, 240, 153],
                                    [156, 237, 149], [155, 235, 145], [155, 232, 142], [155, 230, 138], [155, 227, 134], [156, 224, 130], [156, 222, 126], [157, 219, 123], [157, 217, 119], [158, 214, 116], [159, 212, 112],
                                    [160, 209, 109], [161, 207, 105], [162, 204, 102], [163, 201, 99], [165, 199, 95], [166, 196, 92], [168, 194, 89], [169, 191, 86], [171, 189, 83], [172, 186, 80], [174, 184, 77],
                                    [176, 181, 74], [177, 179, 71], [176, 173, 69], [173, 166, 66], [171, 159, 63], [168, 152, 61], [166, 146, 58], [163, 139, 55], [161, 132, 53], [158, 125, 51], [156, 118, 48],
                                    [153, 112, 46], [150, 105, 44], [148, 98, 41], [145, 92, 39], [143, 85, 37], [140, 79, 35], [138, 72, 33], [135, 66, 31], [133, 60, 29], [130, 53, 27], [128, 47, 25],
                                    [125, 41, 24], [122, 36, 22], [120, 30, 20], [117, 24, 19], [115, 19, 17], [112, 16, 18], [110, 14, 20], [107, 13, 23], [105, 12, 25], [102, 10, 27], [99, 9, 29],
                                    [97, 8, 31], [94, 7, 33], [92, 6, 35], [89, 4, 37], [87, 3, 39], [84, 3, 40], [82, 2, 42], [79, 1, 43], [77, 0, 45], [80, 2, 47], [84, 3, 50],
                                    [87, 5, 53], [91, 7, 56], [94, 9, 59], [98, 12, 62], [101, 14, 65], [105, 17, 68], [109, 20, 72], [112, 22, 75], [116, 25, 78], [119, 29, 82], [123, 32, 85],
                                    [126, 35, 89], [130, 39, 92], [134, 43, 96], [137, 47, 99], [141, 51, 103], [144, 55, 107], [148, 59, 111], [151, 64, 115], [155, 68, 119], [159, 73, 123], [162, 78, 127],
                                    [166, 83, 131], [169, 88, 135], [173, 93, 140], [176, 99, 144], [180, 104, 149], [184, 110, 153], [187, 116, 158], [191, 122, 162], [194, 128, 167], [198, 135, 171], [201, 141, 176],
                                    [205, 148, 181], [209, 154, 186], [212, 161, 191], [216, 168, 196], [219, 175, 201], [223, 183, 206], [226, 190, 211], [230, 198, 217], [234, 206, 222], [237, 213, 227], [241, 221, 233],
                                    [244, 230, 238], [248, 238, 244], [251, 246, 249], [255, 255, 255], [250, 250, 250], [245, 245, 245], [240, 240, 240], [235, 235, 235], [230, 230, 230], [224, 224, 224], [219, 219, 219],
                                    [214, 214, 214], [209, 209, 209], [204, 204, 204], [199, 199, 199], [194, 194, 194], [189, 189, 189], [184, 184, 184], [179, 179, 179], [173, 173, 173], [168, 168, 168], [163, 163, 163],
                                    [158, 158, 158], [153, 153, 153], [148, 148, 148], [143, 143, 143], [138, 138, 138], [133, 133, 133], [128, 128, 128], [122, 122, 122], [117, 117, 117], [112, 112, 112], [107, 107, 107],
                                    [102, 102, 102], [97, 97, 97], [92, 92, 92], [87, 87, 87], [82, 82, 82], [77, 77, 77], [71, 71, 71], [66, 66, 66], [61, 61, 61], [56, 56, 56], [51, 51, 51],
                                    [46, 46, 46], [41, 41, 41], [36, 36, 36], [31, 31, 31], [26, 26, 26], [20, 20, 20], [15, 15, 15], [10, 10, 10], [5, 5, 5], [0, 0, 0]]) / 256.
        elif colormap == 'ck_BlueRedBlack':
            colorvalues = np.array([[256,256,256], [0,0,0], [0,0,256], [256,0,0], [0,0,0]])/256.
        elif colormap == 'ck_BlueBlackRed':
            colorvalues = np.array([[256,256,256], [0,0,0], [0,0,256], [0,0,0], [256,0,0]])/256.
        else:
            #raise RuntimeError('colormap name must be either a pyngl named colormap or else from the list of user-defined ones')
            colorvalues = colormap
        return colorvalues
        

def map_proj_setup(resources, lon=None, lat=None, polar=None, projection=None, latlimits=None, lonlimits=None, nomaplimits=None, latcenter=None, loncenter=None, grid=None, specialprojection=None, OutlineBoundarySets=None, thinshorelines=False):
    # set up map projection and update NGL resource file as such
    #
    # first some predefine special cases
    if specialprojection != None:
        if specialprojection=="namer_satellite":
            loncenter=-100.
            latcenter=40.
            lonlimits=[-130.,-70.]
            latlimits=[10., 77.]
            projection="Satellite"
        elif specialprojection=='namer' or specialprojection=="namer_states":
            lonlimits=[-170.,-53.]
            latlimits=[12.5, 72.]
            projection="CylindricalEquidistant"
        elif specialprojection=="namer_camer_satellite":
            loncenter=-90.
            latcenter=25.
            lonlimits=[-130.,-50.]
            latlimits=[0., 90.]
            projection="Satellite"
        elif specialprojection=="polar_satellite":
            polar=True
            latcenter=90.
            latlimits=[0., 90.]
            projection="orthographic"
        elif specialprojection=="polar_stereo":
            polar=True
            latcenter=90.
            latlimits=[45., 90.]
            projection="Stereographic"
        elif specialprojection=="global_noant":
            # someday I am going to figure out how to make the data go from -185 to +175 but for now it doesn't work
            projection='CylindricalEquiDistant'
            polar=False
            nomaplimits=False
            latlimits=[-60.,90.]
            lonlimits=[-175.,185.]
        elif specialprojection=="global":
            # someday I am going to figure out how to make the data go from -185 to +175 but for now it doesn't work
            polar=False
            nomaplimits=False
            projection='CylindricalEquiDistant'
            latlimits=[-90.,90.]
            lonlimits=[-175.,185.]
        elif specialprojection=="conus" or specialprojection=="conus_states":
            loncenter=-97.5
            latcenter=36.5
            lonlimits=[-125.,-70.]
            latlimits=[23., 50.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="conus1" or specialprojection=="conus_states1":
            loncenter=-96.25
            latcenter=36.75
            lonlimits=[-120,-72.5]
            latlimits=[25.5, 49.75]
            projection="CylindricalEquiDistant"
        elif specialprojection=="calif":
            loncenter=-118.75
            latcenter=37.
            lonlimits=[-125.,-112.5]
            latlimits=[31., 43.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="calif2":
            loncenter=-121.
            latcenter=37.
            lonlimits=[-125.,-117]
            latlimits=[31., 43.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="westus":
            loncenter=-114.25
            latcenter=40.
            lonlimits=[-123.5,-104.]
            latlimits=[31., 49.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="westus_ext":
            loncenter=-115.5
            latcenter=40.
            lonlimits=[-127.0,-104.]
            latlimits=[31., 49.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="samer_satellite":
            latlimits=[-60.,15.]
            lonlimits=[-90,-30]
            projection='satellite'
            latcenter=-15
            loncenter=-60
        elif specialprojection=="samer":
            latlimits=[-60.,15.]
            lonlimits=[-90,-30]
            projection='CylindricalEquidistant'
        elif specialprojection=="alaska":
            latlimits=[54.,72.]
            lonlimits=[-168,-142]
            projection='CylindricalEquidistant'
        elif specialprojection=="alaska1":
            latlimits=[52.,72.]
            lonlimits=[-170.,-132.]
            projection='CylindricalEquidistant'
        elif specialprojection=="conus_states_rect":
            lonlimits=[-130.,-60.]
            latlimits=[23., 60.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="eurasia_countries":
            lonlimits=[-12.,180.]
            latlimits=[5., 80.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="europe":
            lonlimits=[-25.,80]
            latlimits=[20., 75.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="asia":
            lonlimits=[50.,170.]
            latlimits=[5., 80.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="africa":
            lonlimits=[-20.,55.]
            latlimits=[-40., 40.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="australia":
            lonlimits=[95.,180.]
            latlimits=[-50., 10.]
            projection="CylindricalEquiDistant"
        elif specialprojection=="boreal_na":
            latlimits=[50.,80.]
            lonlimits=[-170.,-90.]
            projection='satellite'
            latcenter=65.
            loncenter=-130.
        else:
            raise NotImplmentedError
    # next set up the map projection based on arguments
    #
    resources.sfXArray        = lon[:]
    resources.sfXCStartV = np.float(np.min(lon))
    resources.sfXCEndV   = np.float(np.max(lon))
    resources.sfYArray        = lat[:]
    resources.sfYCStartV = np.float(np.min(lat))
    resources.sfYCEndV   = np.float(np.max(lat))
    resources.mpProjection = projection
    resources.mpGridAndLimbOn =  grid
    if thinshorelines:
        resources.mpGeophysicalLineThicknessF = 0.2
    else:
        resources.mpGeophysicalLineThicknessF = 2.        
    #
    if OutlineBoundarySets != None:
        resources.mpOutlineBoundarySets = OutlineBoundarySets
    #
    if specialprojection=="conus" or specialprojection=="eurasia_countries" or specialprojection == "namer"  or specialprojection == "samer" or specialprojection=="europe" or specialprojection=="asia" or specialprojection=="africa" or specialprojection=="australia" or specialprojection=="alaska1":
        resources.mpOutlineBoundarySets = "National"
        resources.mpGridAndLimbOn =  False
        resources.mpNationalLineThicknessF = 1.5
    if specialprojection=="conus_states" or specialprojection=="conus_states_rect" or specialprojection=="namer_states" or specialprojection=="calif" or specialprojection=="calif2" or specialprojection=="conus_states1" or specialprojection=="westus_ext" or specialprojection=="westus":
        resources.mpOutlineBoundarySets = "AllBoundaries"
        resources.mpGridAndLimbOn =  False
        resources.mpNationalLineThicknessF = 1.5
        resources.mpUSStateLineThicknessF = 1.0
    #
    if polar==None:
        if lat.min() < 50:
            polar=False
        else:
            polar=True
    #
    if polar:
        if projection == "CylindricalEquidistant" or projection== "Stereographic":
            resources.mpLimitMode           = "LatLon"   # Specify area of map
            resources.mpEllipticalBoundary  = True
            projection="Stereographic"
            resources.mpCenterLatF          = 90.
            if latlimits == None:
                resources.mpMaxLatF             = 90.        # to zoom in on.
                resources.mpMinLatF             = 49.
            else:
                resources.mpMaxLatF             = latlimits[1]        # to zoom in on.
                resources.mpMinLatF             = latlimits[0]
        elif projection == "satellite" or projection == "orthographic":
            resources.mpLimitMode           = "LatLon"   # Specify area of map
            resources.mpEllipticalBoundary  = True
            resources.mpCenterLatF          = 90.
            resources.mpCenterLonF          = 0.
            # if latlimits == None:
            #     resources.mpMaxLatF             = 90.        # to zoom in on.
            #     resources.mpMinLatF             = 49.
            # else:
            #     resources.mpMaxLatF             = latlimits[1]        # to zoom in on.
            #     resources.mpMinLatF             = latlimits[0]
    elif projection == "Robinson":
        resources.mpLimitMode           = "MaximalArea"
        resources.mpCenterLatF          = 0.
        resources.mpCenterLonF          = 11.
        resources.mpPerimOn = False
        resources.mpGridAndLimbOn =  True
        resources.mpGridLineColor   = "transparent"     # we don't want lat/lon lines
        resources.pmTickMarkDisplayMode    = "Never"     # Don't draw tickmark border.
    else:
        resources.mpLimitMode           = "LatLon"   # Specify area of map
        if not nomaplimits:
            if latlimits == None:
                resources.mpMaxLatF             = np.max(lat[:])        # to zoom in on.
                resources.mpMinLatF             = np.min(lat[:])
                # resources.mpCenterLatF          = np.min(lat[:]) + (np.max(lat[:])-np.min(lat[:]))/2.
            else:
                resources.mpMaxLatF             = latlimits[1]
                resources.mpMinLatF             = latlimits[0]
                # resources.mpCenterLatF          = latlimits[0] + 0.5*(latlimits[1] - latlimits[0])
            if lonlimits == None:
                resources.mpMaxLonF             = np.max(lon[:])        # to zoom in on.
                resources.mpMinLonF             = np.min(lon[:])
                # resources.mpCenterLonF          = np.min(lon[:]) + (np.max(lon[:])-np.min(lon[:]))/2.
            else:
                resources.mpMaxLonF             = lonlimits[1]
                resources.mpMinLonF             = lonlimits[0]
                # resources.mpCenterLonF          = lonlimits[0] + 0.5*(lonlimits[1] - lonlimits[0])
        if latcenter != None:
            resources.mpCenterLatF          = latcenter
        if loncenter != None:
            resources.mpCenterLonF          = loncenter


def fill(data, lat, lon, polar=None, projection="CylindricalEquidistant", filltype="cell", contour=False, levels=None, file=None, outline_cells=None, title=None, subtitle=None, level_colors=None, aspect_ratio=None, latlimits=None, lonlimits=None, grid=False, latcenter=None, loncenter=None, specialprojection=None, nomaplimits=False, vector_delta_lat=None, vector_delta_lon=None, vector_lat=None, vector_lon=None, vector_greatcircle=True, vector_arrowheadlength=1.5, vector_arrowheadwidth=1.5, vector_color=None, vector_arrow_thickness=1., vector_arrows_forwards=True, colormap="wh-bl-gr-ye-re", overlay_contour_data=None, overlay_contour_levels=None, overlay_contour_lat=None, overlay_contour_lon=None, overlay_contour_colors=None, overlay_contour_thickness=None, overlay_contour_patterns=None, suppress_colorbar=False, suppress_latlonlabels=False, inset_title=None, inset_title_x=None, inset_title_y=None, inset_title_y_list=None, inset_title_x_list=None, inset_title_colors=None, inset_title_yspace=None, inset_title_xspace=0., inset_title_fontsize=0.025, max_ws_size=None, contour_fill=False, override_boundaries=None, station_names=None, station_lats=None, station_lons=None, station_symbol="star_5point", add_colors=None, OutlineBoundarySets=None, reverse_colors=False, expand_colormap_middle=None, thinshorelines=False, overlay_polyline_x=None, overlay_polyline_y=None, overlay_polyline_color=None, overlay_polyline_thickness=None, overlay_polyline_dashpattern=None, makepng=False, png_dens=pngdens, showjupyter=False, plot_lat_profiles=None, plot_lat_profile_colors=None):

    if showjupyter and type(file)==type(None):
        file = 'temp_fig_file'

    if len(lat.shape) == 1 and len(lon.shape) == 1:
        JM = lat.shape[0]
        IM = lon.shape[0]
    else:
        JM = lat.shape[0]
        IM = lat.shape[1]
        
    data = np.squeeze(data[:])

    if data.shape != (JM,IM):
        raise SizeMismatchError

    plot_type = get_workstation_type(file)

    if len(lon.shape) == 1:
        if np.abs(lon[0] - lon[IM-1]) > 350.:
            try:
                data, lon = Ngl.add_cyclic(data[:], lon[:])
                #             lon_new = np.zeros(IM+1)
                #             lon_new[0:IM] = lon[:]
                #             lon_new[IM] = lon[0]+360.
                #             data = data_new
                #             lon=lon_new
                IM = IM+1
                added_cyclic = True
            except:
                if isinstance(data, np.ma.MaskedArray):
                    data_new = np.ma.masked_all([JM,IM+1])
                else:
                    data_new = np.zeros([JM,IM+1])
                data_new[:,:IM] = data[:,:]
                data_new[:,IM] = data[:,0]
                lon_new = np.zeros(IM+1)
                lon_new[:IM] = lon[:]
                lon_new[IM] = lon[0]
                data = data_new
                lon = lon_new
                IM = IM+1
                print('excepted')
                added_cyclic = True
        else:
            added_cyclic=False
    else:
        added_cyclic=False


    wks_res = Ngl.Resources()

    if file == None:
        wks_res.wkPause = True
    else:
        wks_res.wkPaperHeightF = page_height
        wks_res.wkOrientation = "portrait"
        if type(plot_lat_profiles) == type(None):
            wks_res.wkPaperWidthF = page_width
        else:
            wks_res.wkPaperWidthF = page_width * 1.3

    mp_resources = Ngl.Resources()
    mp_resources.cnFillOn          = True
    mp_resources.cnLinesOn         = contour
    mp_resources.cnLineLabelsOn    = False


    ## for backwards compatibility, do this:
    if filltype=="cell" and contour_fill==True:
        filltype="contour"
    
    if filltype == "cell":
        mp_resources.cnFillMode        = "CellFill"
        mp_resources.cnRasterSmoothingOn = False
    elif filltype == "contour":
        mp_resources.cnFillMode        = "AreaFill"
        mp_resources.cnRasterSmoothingOn = True
    elif filltype == "raster":
        mp_resources.cnFillMode        = "RasterFill"
        mp_resources.cnRasterSmoothingOn = False
        mp_resources.cnRasterMinCellSizeF  = 0.0002
        # mp_resources.cnRasterCellSizeF = 0.00005
        # mp_resources.cnRasterSampleFactorF = 1.
    else:
        raise RuntimeError('wrong value for filltype; must be either "cell" (for showing discrete gridcells), "contour" (for filled contour maps), or "raster" (rasterize the image).')
        

    #     if added_cyclic:
    #         mp_resources.sfXArray        = lon[0:IM-1]
    #         mp_resources.sfXCStartV = np.float(np.min(lon[0:IM-1]))
    #         mp_resources.sfXCEndV   = np.float(np.max(lon[0:IM-1]))
    #     else:

    map_proj_setup(mp_resources, lon=lon, lat=lat, polar=polar, projection=projection, latlimits=latlimits, lonlimits=lonlimits, nomaplimits=nomaplimits, latcenter=latcenter, loncenter=loncenter, grid=grid, specialprojection=specialprojection, OutlineBoundarySets=OutlineBoundarySets, thinshorelines=thinshorelines)

    if override_boundaries != None:
        ### valid options are:  NoBoundaries, Geophysical, National, USStates, GeophysicalAndUSStates, AllBoundaries
        mp_resources.mpOutlineBoundarySets = override_boundaries
    
    if suppress_colorbar == False:
        mp_resources.lbOrientation         = "horizontal"
        mp_resources.lbPerimThicknessF     = 2.
        mp_resources.lbTitleFontThicknessF = 1.5
        mp_resources.lbLabelStride         = 1
        mp_resources.lbRightMarginF        = 0.15
        mp_resources.lbLeftMarginF         = 0.15
        mp_resources.lbTopMarginF           = 0.
        mp_resources.lbBottomMarginF        = 0.5
        mp_resources.lbLabelFontHeightF     = 0.02
    else:
        mp_resources.lbLabelBarOn = False

    if type(levels) == type(None):
        mp_resources.cnMaxLevelCount      = 15
    else:
        mp_resources.cnLevelSelectionMode      = 'ExplicitLevels'
        mp_resources.cnLevels = levels
    mp_resources.nglFrame = False
    mp_resources.nglDraw = True

    if type(plot_lat_profiles) != type(None):
        mp_resources.nglMaximize = False

    if suppress_latlonlabels == True:
        mp_resources.tmXBLabelsOn	    = False
        mp_resources.tmXTLabelsOn	    = False
        mp_resources.tmYLLabelsOn	    = False
        mp_resources.tmYRLabelsOn	    = False
    
    if title != None:
        mp_resources.tiMainString = title
        
    if subtitle != None:
        mp_resources.lbTitleString = subtitle
        mp_resources.lbTitleFontHeightF = 0.02

    if aspect_ratio != None:
        if aspect_ratio > 1.:
            mp_resources.vpHeightF =  0.6  / aspect_ratio
        else:
            mp_resources.vpWidthF =  0.6  * aspect_ratio

    if vector_delta_lat != None and vector_delta_lon != None:
        mp_resources.cnFillDrawOrder = "PreDraw"
        mp_resources.mpFillDrawOrder = "PreDraw"
        mp_resources.tfPolyDrawOrder = "Postdraw"

    if level_colors != None:
        mp_resources.cnFillColors  = level_colors

    wks = Ngl.open_wks(plot_type,file,wks_res)
    if wks < 0 and plot_type == "x11":
        clear_oldest_x11_window()
        wks = Ngl.open_wks(plot_type,file,wks_res)

    if max_ws_size != None:  # this is to avoid an error when making big plots
        ws_id = Ngl.get_workspace_id()
        rlist = Ngl.Resources()
        rlist.wsMaximumSize = max_ws_size
        Ngl.set_values(ws_id,rlist)

    if reverse_colors:
        mp_resources.nglSpreadColorStart = -1
        mp_resources.nglSpreadColorEnd = 2

    colormap = parse_colormap(colormap)
    
    Ngl.define_colormap(wks, colormap)

    if expand_colormap_middle != None:
        cmap = Ngl.get_MDfloat_array(wks, "wkColorMap")
        cmap_length_old = cmap.shape[0]
        center = (cmap_length_old - 1 ) / 2 + 1
        cmap_length_new = cmap_length_old + expand_colormap_middle - 1
        cmap_new = np.zeros([cmap_length_new, 3])
        cmap_new[0:center,:] = cmap[0:center,:]
        cmap_new[center:center+expand_colormap_middle,:] = cmap[center,:]
        cmap_new[center+expand_colormap_middle:cmap_length_new,:] = cmap[center+1:cmap_length_old,:]
        rlist = Ngl.Resources()
        rlist.wkColorMap = cmap_new
        Ngl.set_values(wks,rlist)

    if add_colors != None:
        print((add_colors.shape))
        cmap = Ngl.get_MDfloat_array(wks, "wkColorMap")
        cmap_length_old = cmap.shape[0]
        cmap_length_new = cmap_length_old + add_colors.shape[0]
        cmap_new = np.zeros([cmap_length_new, 3])
        cmap_new[0:cmap_length_old,:] = cmap[0:cmap_length_old,:]
        cmap_new[cmap_length_old:cmap_length_old+add_colors.shape[0],:] = add_colors[:]
        print((cmap_new.shape))
        rlist = Ngl.Resources()
        rlist.wkColorMap = cmap_new
        Ngl.set_values(wks,rlist)
        if reverse_colors:
            mp_resources.nglSpreadColorStart = -1 - add_colors.shape[0]
            mp_resources.nglSpreadColorEnd = 2
        else:
            mp_resources.nglSpreadColorStart = 2
            mp_resources.nglSpreadColorEnd = -1 - add_colors.shape[0]
            
        

    plot = Ngl.contour_map(wks,data,mp_resources)

    if outline_cells != None:
        resources = Ngl.Resources()
        resources.gsLineThicknessF = 3.0
        ### assume uniform grid spacing here...
        res_lon = lon[1]-lon[0]
        res_lat = lat[1]-lat[0]
        if added_cyclic:
            outline_cells = Ngl.add_cyclic(outline_cells)
        ### issues if there are edges that need to be outlined
        for i in range(1,IM-1):
            for j in range(1,JM-1):
                if outline_cells[j,i]:
                    if not outline_cells[j,i-1]:
                        pline = Ngl.add_polyline(wks, plot, [lon[i]-res_lon/2.,lon[i]-res_lon/2.], [lat[j]-res_lat/2.,lat[j]+res_lat/2.], resources)
                    if not outline_cells[j,i+1]:
                        pline = Ngl.add_polyline(wks, plot, [lon[i]+res_lon/2.,lon[i]+res_lon/2.], [lat[j]-res_lat/2.,lat[j]+res_lat/2.], resources)
                    if not outline_cells[j-1,i]:
                        pline = Ngl.add_polyline(wks, plot, [lon[i]-res_lon/2.,lon[i]+res_lon/2.], [lat[j]-res_lat/2.,lat[j]-res_lat/2.], resources)
                    if not outline_cells[j+1,i]:
                        pline = Ngl.add_polyline(wks, plot, [lon[i]-res_lon/2.,lon[i]+res_lon/2.], [lat[j]+res_lat/2.,lat[j]+res_lat/2.], resources)
        #
        #Ngl.draw(plot)

    ## overlay_contours
    if type(overlay_contour_data) != type(None):

        # 
        # Copy just the contour resources from mpres to a new resource list (cnres).
        #
        cnres = Ngl.Resources()
        for t in dir(mp_resources):
          if (t[0:2] == 'cn' or t[0:2] == 'sf' or t[0:3] == 'ngl'):
              setattr(cnres,t,getattr(mp_resources,t))
        #
        if type(overlay_contour_lon) != type(None):
            cnres.sfXArray        = overlay_contour_lon[:]
        else:
            cnres.sfXArray        = lon[:]                
        if type(overlay_contour_lon) != type(None):
            cnres.sfYArray        = overlay_contour_lat[:]
        else:
            cnres.sfYArray        = lat[:]        
        #
        if type(overlay_contour_patterns) == type(None):
            cnres.cnFillOn          = False
            cnres.cnLinesOn         = True
        else:
            cnres.cnFillOn          = True
            cnres.cnLinesOn         = False
            cnres.cnFillMode        = 'AreaFill'
        cnres.nglDraw = False
        cnres.nglFrame = False
        cnres.lbLabelBarOn = False
        cnres.lbLabelsOn = False
        cnres.cnInfoLabelOn = False
        if type(overlay_contour_levels) != type(None):
            cnres.cnLevelSelectionMode      = 'ExplicitLevels'
            cnres.cnLevels = overlay_contour_levels
        cnres.cnLineThicknessF  = 0.2
        if type(overlay_contour_colors) != type(None):
            cnres.cnLineColors = overlay_contour_colors
        if type(overlay_contour_patterns) != type(None):
            cnres.cnFillPatterns = overlay_contour_patterns
            #cnres.cnFillColors = 'Black'
            #cnres.cnFillColor = 'Black'            
            cnres.MonoFillColor = True
            cnres.cnLineDrawOrder      = "Postdraw" # Draw lines and filled
            cnres.cnFillDrawOrder      = "Postdraw" # areas before map gets
            cnres.nglSpreadColorStart     = 1
            cnres.nglSpreadColorEnd     = 1
            #cnres.cnFillDotSizeF  = 0.00001
        if type(overlay_contour_thickness) != type(None):
            cnres.cnLineThicknessF  = overlay_contour_thickness
        #
        contour_overlay = Ngl.contour(wks, overlay_contour_data, cnres)
        Ngl.overlay(plot,contour_overlay)
        Ngl.draw(plot)

    if inset_title != None:
        if type(inset_title) == type(""):
            inset_title_res = Ngl.Resources()
            inset_title_res.txFontHeightF  = inset_title_fontsize
            inset_title_res.txJust  = "CenterLeft"
            txt = Ngl.add_text(wks,plot,inset_title,inset_title_x, inset_title_y,inset_title_res)
        elif type(inset_title) == type([]):
            for inset_title_i in range(len(inset_title)):
                inset_title_res = Ngl.Resources()
                inset_title_res.txFontHeightF  = inset_title_fontsize
                if inset_title_colors != None:
                    inset_title_res.txFontColor = inset_title_colors[inset_title_i]
                if inset_title_y_list == None:
                    inset_title_y_element = inset_title_y + inset_title_yspace*inset_title_i
                else:
                    inset_title_y_element = inset_title_y_list[inset_title_i]
                if inset_title_x_list == None:
                    inset_title_x_element = inset_title_x + inset_title_xspace*inset_title_i
                else:
                    inset_title_x_element = inset_title_x_list[inset_title_i]
                txt = Ngl.add_text(wks,plot,inset_title[inset_title_i],inset_title_x_element, inset_title_y_element, inset_title_res)            
        Ngl.draw(plot)

    if vector_delta_lat != None and vector_delta_lon != None:
        arrow_res = Ngl.Resources()
        if not vector_color == None:
            arrow_res.gsLineColor = vector_color
        arrow_res.gsLineThicknessF = vector_arrow_thickness
        vector_IM = len(vector_lon)
        vector_JM = len(vector_lat)
        vector_pline_id_list = []
        for i in range(vector_IM):
            for j in range(vector_JM):
                try:
                    if not vector_delta_lon.mask[j,i]:
                        # x = np.ma.masked_all(2)
                        # y = np.ma.masked_all(2)
                        # x[0],y[0] = lon[i],lat[j]
                        # x[1],y[1] = lon[i] + vector_delta_lon[j,i], lat[j] + vector_delta_lat[j,i]
                        x0, y0 = vector_lon[i],vector_lat[j]
                        x1, y1 = vector_lon[i] + vector_delta_lon[j,i], vector_lat[j] + vector_delta_lat[j,i]
                        if vector_arrows_forwards:
                            x, y = make_arrow(x0, y0, x1, y1, vector_arrowheadlength, vector_arrowheadwidth, greatcircle=vector_greatcircle)
                        else:
                            x, y = make_arrow(x1, y1, x0, y0, vector_arrowheadlength, vector_arrowheadwidth, greatcircle=vector_greatcircle)                        
                        vector_pline_id_list.append(Ngl.polyline(wks,plot,x,y,arrow_res))
                except:
                    # x = np.ma.masked_all(2)
                    # y = np.ma.masked_all(2)
                    # x[0],y[0] = lon[i],lat[j]
                    # x[1],y[1] = lon[i] + vector_delta_lon[j,i], lat[j] + vector_delta_lat[j,i]
                    x0, y0 = vector_lon[i],vector_lat[j]
                    x1, y1 = vector_lon[i] + vector_delta_lon[j,i], vector_lat[j] + vector_delta_lat[j,i]
                    if vectoframer_arrows_forwards:
                        x, y = make_arrow(x0, y0, x1, y1, vector_arrowheadlength, vector_arrowheadwidth, greatcircle=vector_greatcircle)
                    else:
                        x, y = make_arrow(x1, y1, x0, y0, vector_arrowheadlength, vector_arrowheadwidth, greatcircle=vector_greatcircle)                       
                    vector_pline_id_list.append(Ngl.polyline(wks,plot,x,y,arrow_res))


    if station_names != None:
        markersize=40.
        markerthickness=3.0
        for i in range(len(station_names)):
            resources = Ngl.Resources()
            resources.gsMarkerSizeF = markersize
            resources.gsMarkerThicknessF  = markerthickness
            resources.gsMarkerIndex = station_symbol
            pmarker = Ngl.add_polymarker(wks, plot, station_lons[i], station_lats[i], resources)
            resources = Ngl.Resources()
            resources.txFontHeightF = 20.
            resources.txFontThicknessF = 200.
            resources.txJust = "CenterLeft"
            Ngl.add_text(wks,plot,station_names[i],station_lons[i]+1.,station_lats[i],resources)
        Ngl.draw(plot)


    if type(overlay_polyline_x) != type(None):
        resources = Ngl.Resources()
        if type(overlay_polyline_color) != type(None):
            resources.gsLineColor = overlay_polyline_color
        if type(overlay_polyline_thickness) != type(None):
            resources.gsLineThicknessF = overlay_polyline_thickness
        if type(overlay_polyline_dashpattern) != type(None):
            resources.gsLineDashPattern = overlay_polyline_dashpattern
        overlay_polyline = Ngl.polyline(wks, plot, overlay_polyline_x, overlay_polyline_y, resources)

    if type(plot_lat_profiles) != type(None):
        latprof_res = Ngl.Resources()
        latprof_res.nglMaximize = False
        latprof_res.vpXF = 0.83
        latprof_res.vpYF = 0.65
        latprof_res.vpHeightF = 0.3
        latprof_res.vpWidthF = 0.15
        #
        latprof_res.tmXBMinorOn    = False
        latprof_res.tmYLMinorOn    = False
        latprof_res.tmXBPrecision = 1
        latprof_res.tmXBMaxTicks = 5
        #
        borderlinethickness = 1.
        latprof_res.tmBorderThicknessF = borderlinethickness
        latprof_res.xyLineThicknessF = 1.
        latprof_res.tmXBMajorThicknessF = borderlinethickness
        latprof_res.tmXTMajorThicknessF = borderlinethickness
        latprof_res.tmYRMajorThicknessF = borderlinethickness
        latprof_res.tmYLMajorThicknessF = borderlinethickness        
        #
        if type(plot_lat_profile_colors) != type(None):
            latprof_res.xyLineColors = plot_lat_profile_colors
        Ngl.xy(wks, plot_lat_profiles, lat, latprof_res)
                
    if not file==None:
        Ngl.delete_wks(wks)
        #
        if makepng or showjupyter:
            pdf_to_png(file, density=png_dens)
        if jupyter_avail and showjupyter:
            print(' ')
            display(Image(file+'.png'))
    else:
        x11_window_list.append(wks)

   

################################################################################

def xyplot(x, y, file=None, dots=False, regress=False, title=None, xtitle=None, ytitle=None, xrange=None, yrange=None, colors=None, labels=None, labelorder=None, labelcolors=None, linethickness=2.5, line_opacity=1., overlay_x=None, overlay_y=None, overlay_color=None, overlay_linethickness=2.5, overlay_dots=False, colormap=None, overlay_labels=None, overlay_labelorder=None, overlay_altyaxis=None, overlay_altyaxistitle=None, noyticks=False, noxticks=False, nominorticks=False, norightticks=False, notopticks=False, smallticks=True, outsideticks=True, errorbars=None, overlay_errorbars=None, barwidth=None, dashpattern=None, overlay_dashpattern=None, dashlabels=None, dashlabelpatterns=None, label_xstart=None, label_ystart=None, label_yspace=None, polygons=False, shadederror_thickness=None, shadederror_color=None, shadederror_fillpattern=None, shadederror_thickness_yindepvar=None, labelfontsize=.02, overlaylabelfontsize=None, overlaylabelxstart=None, overlaylabelystart=None, overlaylabel_yspace=None, overlaylabel_xspace=None, aspect_ratio=None, title_charsize=0.75, xlog=False, ylog=False, yreverse=False, box_whisker_plot=False, stack_shade_values=False, minobs_boxplot=3, dotsize=0.02, Nonemask=False, hline=None, hline_color=None, hline_dashpattern=None, vline=None, vline_color=None, vline_dashpattern=None, shaded_dot_data=None, shaded_dot_levels=None, shaded_line_data=None, shaded_line_levels=None, subtitle=None, vband=None, hband=None, overlay_vectors_x=None, overlay_vectors_y=None, overlay_vectors_arrowheadlength=None, overlay_vectors_arrowheadwidth=None, overlay_vectors_forwards=True, overlay_vectors_thickness=1.0, shaded_vectors_data=None, shaded_vectors_levels=None, inset_title=None, inset_title_x=None, inset_title_y=None, inset_title_fontsize=0.03, inset_textjust="CenterRight", overlay_shadederror_thickness=None, nobottomticks=False, label_xspace=None, print_regression_stats=False, shadederror_ulimit=None, shadederror_llimit=None, shadederror_opacity=None, overlay_ellipses_x=None, overlay_ellipses_y=None, overlay_ellipses_xaxis=None, overlay_ellipses_yaxis=None, overlay_ellipses_angle=None, overlay_ellipse_thickness=None, overlay_ellipses_filled=False, overlay_ellipses_opacity=None, overlay_ellipses_color=None, shuffle_shaded_dots=False, shuffle_shaded_lines=False, makepng=False, png_dens=pngdens, use_wks=None, overlay_shadederror_ulimit=None, overlay_shadederror_llimit=None, showjupyter=False):

    if showjupyter and type(file)==type(None):
        file = 'temp_fig_file'

    if use_wks == None:
        plot_type = get_workstation_type(file)
        
        if  Nonemask:
            if isinstance(x, list):
                x = Nonemask(x)            
            if isinstance(y, list):
                y = Nonemask(y)
            if isinstance(overlay_x, list):
                overlay_x = Nonemask(overlay_x)
            if isinstance(overlay_y, list):
                overlay_y = Nonemask(overlay_y)
                
        if isinstance(x, np.ma.masked_array) or isinstance(y, np.ma.masked_array):
            masked_input = True
        else:
            masked_input = False
            
        wks_res = Ngl.Resources()
        if plot_type == 'x11':
            wks_res.wkPause = False
        elif plot_type == 'png':
            wks_res.wkWidth = page_width * 100
            wks_res.wkHeight = page_height * 100
        else:
            wks_res.wkPaperWidthF = page_width
            wks_res.wkPaperHeightF = page_height
            wks_res.wkOrientation = "portrait"
            
        if not colormap == None:
            colormap = parse_colormap(colormap)
            wks_res.wkColorMap = colormap
            
        wks = Ngl.open_wks(plot_type,file,wks_res)
        if wks < 0 and plot_type == "x11":
            clear_oldest_x11_window()
            wks = Ngl.open_wks(plot_type,file,wks_res)
    else:
        wks = use_wks

    resources = Ngl.Resources()

    #cdkif plot_type != 'png':
    resources.nglDraw = False

    #cdkif plot_type != 'png':
    resources.nglFrame = False

    if title != None:
        resources.tiMainString = title

    if xtitle != None:
        resources.tiXAxisString = xtitle

    if ytitle != None:
        resources.tiYAxisString = ytitle

    resources.tiMainFontHeightF = 0.025 * title_charsize

    if yrange != None:
        resources.trYMinF = np.min(yrange)
        resources.trYMaxF = np.max(yrange)
    else:
        if not ylog:
            yrange = [np.ma.min(y), np.ma.max(y)]

    if yreverse:
        resources.trYReverse   = True

    if xrange != None:
        resources.trXMinF = np.min(xrange)
        resources.trXMaxF = np.max(xrange)
    else:
        if not xlog:
            xrange = [np.ma.min(x), np.ma.max(x)]

    if ylog:
        resources.xyYStyle = "Log"

    if xlog:
        resources.xyXStyle = "Log"
    
    if dots:
        resources.xyMarkLineMode = 'Markers'
        resources.xyMarker = 1
        if colors != None:
            if type(colors) == type(0) or type(colors) == type("hello"):
                resources.xyMarkerColor = colors
            else:
                resources.xyMarkerColors = colors
        resources.xyMarkerSizeF = dotsize

    else:
        resources.xyLineThicknessF = linethickness
        resources.xyLineOpacityF = line_opacity

    if type(colors) != type(None):
        resources.xyLineColors = colors


    if smallticks:
        resources.tmXBMajorLengthF   = 0.01
        resources.tmXBMinorLengthF   = 0.005
        resources.tmYLMajorLengthF   = 0.01
        resources.tmYLMinorLengthF   = 0.005

    if outsideticks:
        resources.tmXBMajorOutwardLengthF = resources.tmXBMajorLengthF
        resources.tmXBMinorOutwardLengthF = resources.tmXBMinorLengthF
        resources.tmYLMajorOutwardLengthF = resources.tmYLMajorLengthF
        resources.tmYLMinorOutwardLengthF = resources.tmYLMinorLengthF

    if noyticks:
        resources.tmYLLabelsOn    = False
        resources.tmYLOn          = False
        resources.tmYROn          = False

    if noxticks:
        resources.tmXBLabelsOn    = False
        resources.tmXTOn          = False
        resources.tmXBOn          = False

    if norightticks or overlay_altyaxis != None:
        resources.tmYROn          = False

    if notopticks:
        resources.tmXTOn          = False

    if nobottomticks:
        resources.tmXBOn          = False
    
    if nominorticks:
        resources.tmXBMinorOn    = False
        resources.tmYLMinorOn    = False

    if dashpattern != None:
        if isinstance(dashpattern, int):
            resources.xyDashPattern = dashpattern
        else:
            resources.xyDashPatterns = dashpattern

    if overlay_altyaxis != None:
        resources.nglMaximize = False
        resources.vpHeightF   = 0.75
        resources.vpWidthF    = 0.65
        resources.vpXF        = 0.20
        resources.vpYF        = 0.90

    if aspect_ratio != None:
        if aspect_ratio > 1.:
            resources.vpHeightF =  0.6  / aspect_ratio
        else:
            resources.vpWidthF =  0.6  * aspect_ratio

    if type(shaded_vectors_data) != type(None):
        # set up labelbar as the colorbar
        lb_res = Ngl.Resources()
        if subtitle != None:
            lb_res.lbTitleString = subtitle
        #
        lb_res.lbOrientation         = "horizontal"
        lb_res.lbPerimThicknessF     = 2.
        lb_res.lbTitleFontThicknessF = 2.
        lb_res.lbLabelStride         = 1
        lb_res.lbRightMarginF        = 0.15
        lb_res.lbLeftMarginF         = 0.15
        lb_res.lbTopMarginF           = 0.
        lb_res.lbBottomMarginF        = 0.5
        lb_res.lbLabelFontHeightF     = 0.02
        #        
        nlevels = len(shaded_vectors_levels)
        cmap = Ngl.retrieve_colormap(wks)
        nbars = nlevels+1
        colorbars = np.arange(nbars) / (nbars-1.) * (cmap.shape[0]-3)
        colorbars_int = np.array(colorbars+2., dtype=np.int32)
        colorbar_x = xrange[0] + (xrange[1]-xrange[0]) * 0.1
        colorbar_y = yrange[0]
        level_label_string_list = []
        for i in range(len(shaded_vectors_levels)):
            level_label_string_list.append(str(shaded_vectors_levels[i]))
        pid = Ngl.labelbar_ndc(wks, nbars, level_label_string_list, colorbar_x, colorbar_y, lb_res)



    if type(shaded_dot_data) == type(None) and type(shaded_line_data) == type(None):
        if not (box_whisker_plot or stack_shade_values):
            plot = Ngl.xy(wks, x, y, resources)
            if xrange == None:
                xrange = [np.ma.min(x), np.ma.max(x)]
            if yrange == None:
                yrange = [np.ma.min(y), np.ma.max(y)]
        else:
            if xrange == None:
                xrange = [np.ma.min(x), np.ma.max(x)]
            resources.trXMinF = np.min(xrange)
            resources.trXMaxF = np.max(xrange)
            if yrange == None:
                yrange = [np.ma.min(y), np.ma.max(y)]
            resources.trYMinF = np.min(yrange)
            resources.trYMaxF = np.max(yrange)

            dummies = np.ma.masked_all(3)
            plot = Ngl.xy(wks, dummies, dummies, resources)
    else:
        # colored dots.  first set up a blank plot
        if xrange == None:
            xrange = [np.ma.min(x), np.ma.max(x)]
        if yrange == None:
            yrange = [np.ma.min(y), np.ma.max(y)]
        if not (xlog or ylog):
            dummies = np.ma.masked_all(3)
        else:
            dummies = np.array([1e-30, 2e-30])
        plot = Ngl.xy(wks, dummies, dummies, resources)
        #
        # now set up labelbar as the colorbar
        lb_res = Ngl.Resources()
        if subtitle != None:
            lb_res.lbTitleString = subtitle
        #
        lb_res.lbOrientation         = "horizontal"
        lb_res.lbPerimThicknessF     = 2.
        lb_res.lbTitleFontThicknessF = 2.
        lb_res.lbLabelStride         = 1
        lb_res.lbRightMarginF        = 0.15
        lb_res.lbLeftMarginF         = 0.15
        lb_res.lbTopMarginF           = 0.
        lb_res.lbBottomMarginF        = 0.5
        lb_res.lbLabelFontHeightF     = 0.02
        #
        if type(shaded_dot_data) != type(None):
            nlevels = len(shaded_dot_levels)
        else:
            nlevels = len(shaded_line_levels)            
        cmap = Ngl.retrieve_colormap(wks)
        nbars = nlevels+1
        colorbars = np.arange(nbars) / (nbars-1.) * (cmap.shape[0]-3)
        colorbars_int = np.array(colorbars+2., dtype=np.int32)
        colorbar_x = xrange[0] + (xrange[1]-xrange[0]) * 0.1
        colorbar_y = yrange[0]
        level_label_string_list = []
        for i in range(nlevels):
            if type(shaded_dot_data) != type(None):
                level_label_string_list.append(str(shaded_dot_levels[i]))
            else:
                level_label_string_list.append(str(shaded_line_levels[i]))                
        # pid = Ngl.labelbar_ndc(wks, nbars, level_label_string_list, colorbar_x, colorbar_y, lb_res)

    if label_xstart == None:
        label_xstart = min(xrange) + (max(xrange)-min(xrange)) * 0.1
    if label_ystart == None:
        label_ystart = max(yrange) - (max(yrange)-min(yrange)) * 0.1
    if label_yspace == None:
        if yreverse:
            label_yspace =  -(max(yrange)-min(yrange)) * 0.05
        else:
            label_yspace =  (max(yrange)-min(yrange)) * 0.05
    if label_xspace == None:
        if not xlog:
            label_xspace = 0.
        else:
            label_xspace = 1.

    if regress:
        if x.shape == y.shape:
            ## rc,attrs = Ngl.regline(x, y)
            import statslib
            b, r_sq = statslib.linreg(x,y)
            if masked_input:
                x0 = np.array([np.ma.min(x), np.ma.max(x)])
            else:
                x0 = np.array([np.min(x), np.max(x)])
            ##  y0 = x0 * rc + attrs['yintercept']
            y0 = x0 * b[1] + b[0]
            resources = Ngl.Resources()
            resources.gsLineThicknessF = 2.
            line = Ngl.add_polyline(wks, plot, x0, y0, resources)
            pstring = []
            if print_regression_stats:
                str_slope = '%s' % float('%.2g' % b[1])
                str_r_sq = '%s' % float('%.2f' % r_sq)
                str_intercept = '%s' % float('%.2g' % abs(b[0]))
                if b[0] >= 0:
                    textline_1 = "y = "+ str_slope + "x + " + str_intercept
                else:
                    textline_1 = "y = "+ str_slope + "x - " + str_intercept                    
                textline_2 = "r~S~2~N~ = " + str_r_sq
                resources = Ngl.Resources()
                resources.txFontHeightF = .02
                resources.txJust = "CenterLeft"
                pstring.extend([Ngl.add_text(wks,plot,textline_1,label_xstart,label_ystart-0*label_yspace,resources)])
                pstring.extend([Ngl.add_text(wks,plot,textline_2,label_xstart,label_ystart-1*label_yspace,resources)])
            else:
                print(r_sq)
        else:
            ## need to loop over repeating axis for a variety of regression lines
            import statslib
            # print(x.shape)
            # print(y.shape)
            ## assume vector x, array y
            for i in range(y.shape[0]):
                try:
                    b, r = statslib.linreg(x,y[i,:])
                except:
                    print('skipped one')
                if masked_input:
                    xmask = np.ma.masked_array(x, mask=y[i,:].mask)
                    x0 = np.array([np.ma.min(xmask), np.ma.max(xmask)])
                else:
                    x0 = np.array([np.min(x), np.max(x)])
                ##  y0 = x0 * rc + attrs['yintercept']
                y0 = x0 * b[1] + b[0]
                resources = Ngl.Resources()
                resources.gsLineThicknessF = 2.
                line = Ngl.add_polyline(wks, plot, x0, y0, resources)

    if errorbars != None:
        if barwidth==None:
            barwidth = 0.2 * (xrange[1]-xrange[0])/x.shape[0]
        if errorbars.shape == x.shape:
            if errorbars.shape == y.shape:
                for i in range(len(errorbars)):
                    resources = Ngl.Resources()
                    resources.gsLineThicknessF = linethickness
                    bar_x = [x[i]-barwidth,x[i]+barwidth,x[i],x[i],x[i]-barwidth,x[i]+barwidth]
                    bar_y = [y[i]+errorbars[i],y[i]+errorbars[i],y[i]+errorbars[i],y[i]-errorbars[i],y[i]-errorbars[i],y[i]-errorbars[i]]
                    poly = Ngl.add_polyline(wks, plot, bar_x, bar_y, resources)
            elif errorbars.shape[0] == y.shape[1]:
                for i in range(len(errorbars)):
                    resources = Ngl.Resources()
                    resources.gsLineThicknessF = linethickness
                    bar_x = [x[i]-barwidth,x[i]+barwidth,x[i],x[i],x[i]-barwidth,x[i]+barwidth]
                    bar_y = [y[0,i]+errorbars[i],y[0,i]+errorbars[i],y[0,i]+errorbars[i],y[0,i]-errorbars[i],y[0,i]-errorbars[i],y[0,i]-errorbars[i]]
                    poly = Ngl.add_polyline(wks, plot, bar_x, bar_y, resources)
            else:
                raise NotImplementedError
                
        else:
            raise NotImplementedError

    if overlay_errorbars != None:
        if barwidth==None:
            barwidth = 0.2 * (xrange[1]-xrange[0])/x.shape[0]
        if overlay_errorbars.shape == overlay_x.shape:
            if overlay_errorbars.shape == overlay_y.shape:
                for i in range(len(overlay_errorbars)):
                    resources = Ngl.Resources()
                    resources.gsLineThicknessF = overlay_linethickness
                    bar_x = [overlay_x[i]-barwidth,overlay_x[i]+barwidth,overlay_x[i],overlay_x[i],overlay_x[i]-barwidth,overlay_x[i]+barwidth]
                    bar_y = [overlay_y[i]+overlay_errorbars[i],overlay_y[i]+overlay_errorbars[i],overlay_y[i]+overlay_errorbars[i],overlay_y[i]-overlay_errorbars[i],overlay_y[i]-overlay_errorbars[i],overlay_y[i]-overlay_errorbars[i]]
                    poly = Ngl.add_polyline(wks, plot, bar_x, bar_y, resources)
            elif overlay_errorbars.shape[0] == overlay_y.shape[1]:
                for i in range(len(errorbars)):
                    resources = Ngl.Resources()
                    resources.gsLineThicknessF = overlay_linethickness
                    bar_x = [overlay_x[i]-barwidth,overlay_x[i]+barwidth,overlay_x[i],overlay_x[i],overlay_x[i]-barwidth,overlay_x[i]+barwidth]
                    bar_y = [overlay_y[0,i]+overlay_errorbars[i],overlay_y[0,i]+overlay_errorbars[i],overlay_y[0,i]+overlay_errorbars[i],overlay_y[0,i]-overlay_errorbars[i],overlay_y[0,i]-overlay_errorbars[i],overlay_y[0,i]-overlay_errorbars[i]]
                    poly = Ngl.add_polyline(wks, plot, bar_x, bar_y, resources)
            else:
                raise NotImplementedError
                
        else:
            raise NotImplementedError

    

    if not (type(overlay_x)==type(None) and type(overlay_y)==type(None)):
        ### overlay line(s) on top. if more than one line, have shape of [a,b]
        ### where a is the number of lines and b is the number of points in each line
        try:
            ndims_overlay_y = np.size(overlay_y.shape)
        except AttributeError:
            ## handle case if overlay_y is a list.  assume it is a 2-d list
            if isinstance(overlay_y, list):
                if type(overlay_y[0]) == list:
                    ndims_overlay_y = 2
                else:
                    ndims_overlay_y = 1
            else:
                raise RuntimeError
        try:
            ndims_overlay_x = np.size(overlay_x.shape)
        except AttributeError:
            ## handle case if overlay_x is a list.  assume it is a 2-d list
            if isinstance(overlay_x, list):
                if type(overlay_x[0]) == list:
                    ndims_overlay_x = 2
                else:
                    ndims_overlay_x = 1
            else:
                raise RuntimeError
        if overlay_altyaxis == None:
            if ndims_overlay_y == 1:
                resources = Ngl.Resources()
                if overlay_dots:
                    # resources.gsMarkLineMode = 'Markers'
                    # resources.gsMarker = 1
                    resources.gsMarkerIndex = 1
                    resources.gsMarkerSizeF = dotsize * 1.5
                    # resources.gsMarkerThicknessF = overlay_linethickness
                    if overlay_color != None:
                        resources.gsMarkerColor = overlay_color
                else:
                    resources.gsLineThicknessF = overlay_linethickness
                if overlay_color != None:
                    resources.gsLineColor = overlay_color
                if overlay_dashpattern != None:
                    resources.gsLineDashPattern = overlay_dashpattern
                ### need to manually handle masked values since add_polyline doesn't seem to do that
                if isinstance(overlay_y, np.ndarray) and isinstance(overlay_x, np.ndarray):
                    polyline_x, polyline_y = handle_masks(overlay_x, overlay_y)
                elif isinstance(overlay_y, list) and isinstance(overlay_x, list):
                    maskedarray_overlayx = Nonemask(overlay_x)
                    maskedarray_overlayy = Nonemask(overlay_y)
                    polyline_x, polyline_y = handle_masks(maskedarray_overlayx, maskedarray_overlayy)
                else:
                    raise RuntimeError
                if overlay_dots:
                    pline = Ngl.add_polymarker(wks, plot, polyline_x, polyline_y, resources)
                else:
                    pline = Ngl.add_polyline(wks, plot, polyline_x, polyline_y, resources)
            elif ndims_overlay_y == 2 and ndims_overlay_x == 1:
                shape_overlay_y = overlay_y.shape
                #          pline = np.zeros(shape_overlay_x[0])
                for i in range(shape_overlay_y[0]):
                    resources = Ngl.Resources()
                    if overlay_dots:
                        # resources.gsMarkLineMode = 'Markers'
                        # resources.gsMarker = 1
                        resources.gsMarkerIndex = 1
                        resources.gsMarkerSizeF = dotsize * 1.5
                    else:
                        if type(overlay_linethickness) == type(1.):
                            resources.gsLineThicknessF = overlay_linethickness
                        else:
                            resources.gsLineThicknessF = overlay_linethickness[i]                            
                    if overlay_color != None:
                        if type(overlay_color) == int or type(overlay_color) == type('a string'):
                            if overlay_color >= 0 or type(overlay_color) == type('a string'):
                                if overlay_dots:
                                    resources.gsMarkerColor = overlay_color
                                else:
                                    resources.gsLineColor = overlay_color
                        else:
                            if overlay_color[i] >= 0:
                                resources.gsLineColor = overlay_color[i]
                    if overlay_dashpattern != None:
                        resources.gsLineDashPattern = overlay_dashpattern[i]
                    ### need to manually handle masked values since add_polyline doesn't seem to do that
                    polyline_x, polyline_y = handle_masks(overlay_x, overlay_y[i,:])
                    if overlay_dots:
                        pline = Ngl.add_polymarker(wks, plot, polyline_x, polyline_y, resources)
                    else:
                        pline = Ngl.add_polyline(wks, plot, polyline_x, polyline_y, resources)
            elif ndims_overlay_y == 2 and ndims_overlay_x == 2:
                # assume each point has its own coordinate
                if isinstance(overlay_y, np.ndarray) and isinstance(overlay_x, np.ndarray):
                    shape_overlay_y = overlay_y.shape
                    shape_overlay_x = overlay_x.shape
                    if shape_overlay_y != shape_overlay_x:
                        raise RuntimeError
                    nlines = shape_overlay_y[0]
                    overlaydata_list = False
                elif isinstance(overlay_y, list) and isinstance(overlay_x, list):
                    if len(overlay_y) != len(overlay_x):
                        raise RuntimeError
                    nlines = len(overlay_y)
                    overlaydata_list = True
                else:
                    raise RuntimeError
                #
                for i in range(nlines):
                    resources = Ngl.Resources()
                    if overlay_dots:
                        # resources.gsMarkLineMode = 'Markers'
                        # resources.gsMarker = 1
                        resources.gsMarkerIndex = 1
                        resources.gsMarkerSizeF = dotsize * 1.5
                    else:
                        if type(overlay_linethickness) == type(1.):
                            resources.gsLineThicknessF = overlay_linethickness
                        else:
                            resources.gsLineThicknessF = overlay_linethickness[i]                            
                    if overlay_color != None:
                        if type(overlay_color) == int or type(overlay_color) == type("string"):
                            if overlay_color >= 0:
                                resources.gsLineColor = overlay_color
                        else:
                            if overlay_color[i] >= 0:
                                resources.gsLineColor = overlay_color[i]
                    if overlay_dashpattern != None:
                        resources.gsLineDashPattern = overlay_dashpattern[i]
                    ### need to manually handle masked values since add_polyline doesn't seem to do that
                    if not overlaydata_list:
                        polyline_x, polyline_y = handle_masks(overlay_x[i,:], overlay_y[i,:])
                    else:
                        maskedarray_overlayx = Nonemask(overlay_x[i])
                        maskedarray_overlayy = Nonemask(overlay_y[i])
                        polyline_x, polyline_y = handle_masks(maskedarray_overlayx, maskedarray_overlayy)
                    if overlay_dots:
                        pline = Ngl.add_polymarker(wks, plot, polyline_x, polyline_y, resources)
                    else:
                        pline = Ngl.add_polyline(wks, plot, polyline_x, polyline_y, resources)
                
            else:
                raise NotImplementedError
        ### separate y axis on right hand side for overlain data
        else:
            res2 = Ngl.Resources()
            res2.tmXBOn       = False
            res2.tmXBLabelsOn = False
            res2.tmXBMinorOn  = False
            res2.tmXTOn       = False
            res2.tmXTLabelsOn = False
            res2.tmXTMinorOn  = False
            res2.tmYLOn       = False
            res2.tmYLLabelsOn = False
            res2.tmYLMinorOn  = False
            res2.tmYRLabelsOn = True
            res2.tmYROn       = True
            res2.tmYUseLeft   = False  
            res2.tmYRFormat   = "f"      # Gets rid of unnecessary trailing zeros
            if overlay_altyaxistitle != None:
                res2.tiYAxisString      = overlay_altyaxistitle
            res2.tiYAxisSide        = "Right"
            if overlay_color != None:
                res2.tiYAxisFontColor   = overlay_color
            res2.trYMinF = np.min(overlay_altyaxis)
            res2.trYMaxF = np.max(overlay_altyaxis)
            res2.trXMinF = Ngl.get_float(plot,"trXMinF")
            res2.trXMaxF = Ngl.get_float(plot,"trXMaxF")
            res2.nglMaximize = False
            res2.vpHeightF   = Ngl.get_float(plot,"vpHeightF")
            res2.vpWidthF    = Ngl.get_float(plot,"vpWidthF")
            res2.vpXF        = Ngl.get_float(plot,"vpXF")
            res2.vpYF        = Ngl.get_float(plot,"vpYF")
            res2.nglFrame = False
            res2.tmYRMajorLengthF   = Ngl.get_float(plot,"tmYRMajorLengthF")
            res2.tmYRMinorLengthF   = Ngl.get_float(plot,"tmYRMinorLengthF")
            if outsideticks:
                res2.tmYRMajorOutwardLengthF = res2.tmYRMajorLengthF
                res2.tmYRMinorOutwardLengthF = res2.tmYRMinorLengthF
            plot2 = Ngl.xy(wks,[0.,0.],[0.,0.],res2)
            if ndims_overlay_y == 1:
                resources = Ngl.Resources()
                resources.gsLineThicknessF = overlay_linethickness
                if overlay_color != None:
                    resources.gsLineColor = overlay_color
                ### need to manually handle masked values since add_polyline doesn't seem to do that
                polyline_x, polyline_y = handle_masks(overlay_x, overlay_y)
                pline = Ngl.add_polyline(wks, plot2, polyline_x, polyline_y, resources)
            elif ndims_overlay_y == 2 and ndims_overlay_x == 1:
                shape_overlay_y = overlay_y.shape
                #          pline = np.zeros(shape_overlay_x[0])
                for i in range(shape_overlay_y[0]):
                    resources = Ngl.Resources()
                    resources.gsLineThicknessF = overlay_linethickness
                    if overlay_color != None:
                        if overlay_color[i] >= 0:
                            resources.gsLineColor = overlay_color[i]
                    ### need to manually handle masked values since add_polyline doesn't seem to do that
                    polyline_x, polyline_y = handle_masks(overlay_x, overlay_y[i,:])
                    pline = Ngl.add_polyline(wks, plot2, polyline_x, polyline_y, resources)
            else:
                raise NotImplementedError
            Ngl.draw(plot2)


    if not inset_title == None:
        if inset_title_x == None:
            inset_title_x = min(xrange) + (max(xrange)-min(xrange)) * 0.95
        if inset_title_y == None:
            if yreverse:
                inset_title_y = max(yrange) - (max(yrange)-min(yrange)) * 0.95
            else:
                inset_title_y = max(yrange) - (max(yrange)-min(yrange)) * 0.05
        resources = Ngl.Resources()
        resources.txFontHeightF = inset_title_fontsize
        resources.txJust = inset_textjust
        Ngl.add_text(wks,plot,inset_title,inset_title_x,inset_title_y,resources)
        
    if not labels==None:
        ### expects labels to be a list of strings
        nlabels = len(labels)
        if labelorder == None:
            labelorder = np.arange(nlabels)
        resources = Ngl.Resources()
        resources.txFontHeightF = labelfontsize
        resources.txJust = "CenterLeft"
        pstring=[]
        for i in range(nlabels):
            # bckgrd_res = deepcopy(resources)
            # bckgrd_res.txFontThicknessF = 2.
            # pstring.extend([Ngl.add_text(wks,plot,labels[i],label_xstart,label_ystart-labelorder[i]*label_yspace,bckgrd_res)])
            if type(labelcolors) != type(None):
                if labelcolors[i] >= 0:
                    resources.txFontColor = labelcolors[i]
            elif type(colors) != type(None):
                if colors[i] >= 0:
                    resources.txFontColor = colors[i]
            if not xlog:
                xpos = label_xstart+labelorder[i]*label_xspace
            else:
                xpos = label_xstart*label_xspace**labelorder[i]
            if not ylog:
                ypos = label_ystart-labelorder[i]*label_yspace
            else:
                ypos = label_ystart/(label_yspace**labelorder[i])
            pstring.extend([Ngl.add_text(wks,plot,labels[i],xpos,ypos,resources)])

    if not overlay_labels==None:
        ### expects labels to be a list of strings
        try:
            nlabels
        except NameError:
            nlabels = 0
        nlabels_overlay = len(overlay_labels)
        if overlay_labelorder == None:
            overlay_labelorder = np.arange(nlabels_overlay)
        resources = Ngl.Resources()
        if overlaylabelfontsize == None:
            overlaylabelfontsize = labelfontsize
        resources.txFontHeightF = overlaylabelfontsize
        resources.txJust = "CenterLeft"
        if overlaylabelxstart == None:
            overlaylabelxstart = label_xstart
        if overlaylabelystart == None:
            overlaylabelystart = label_ystart - nlabels * label_yspace
        if overlaylabel_yspace == None:
            overlaylabel_yspace = label_yspace
        if overlaylabel_xspace == None:
            overlaylabel_xspace = label_xspace
        for i in range(nlabels_overlay):
            if overlay_color != None:
                if type(overlay_color) == type(3) or type(overlay_color) == type("a string"):
                    resources.txFontColor = overlay_color
                else:
                    if overlay_color[i] >= 0:
                        resources.txFontColor = overlay_color[i]
            ### print(overlay_labels[i],overlaylabelxstart,overlaylabelystart+overlay_labelorder[i] * label_yspace)
            pstring = Ngl.add_text(wks,plot,overlay_labels[i],overlaylabelxstart+overlay_labelorder[i] * overlaylabel_xspace,overlaylabelystart+overlay_labelorder[i] * overlaylabel_yspace,resources)
            
    if dashlabels != None and dashlabelpatterns != None:
        try:
            nlabels
        except NameError:
            nlabels = 0
        if label_xstart == None:
            label_xstart = min(xrange) + (max(xrange)-min(xrange)) * 0.1
            label_xend =  min(xrange) + (max(xrange)-min(xrange)) * 0.2
            labelstring_xstart =  min(xrange) + (max(xrange)-min(xrange)) * 0.25
        else:
            label_xend =  (max(xrange)-min(xrange)) * 0.1 + label_xstart
            labelstring_xstart =  (max(xrange)-min(xrange)) * 0.15 + label_xstart
        if label_ystart == None:
            label_ystart = max(yrange) - (max(yrange)-min(yrange)) * 0.1
        if label_yspace == None:
            label_yspace =  (max(yrange)-min(yrange)) * 0.05
        try:
            nlabels_overlay
        except NameError:
            nlabels_overlay = 0
        ndashlabels = len(dashlabels)
        if len(dashlabelpatterns) != ndashlabels:
            raise NotImplementedError
        for i in range(ndashlabels):
            resources = Ngl.Resources()
            resources.gsLineThicknessF = linethickness
            resources.gsLineDashPattern = dashlabelpatterns[i]
            pdashline = Ngl.add_polyline(wks, plot, np.array([label_xstart,label_xend]), np.array([label_ystart-(i+nlabels+nlabels_overlay)*label_yspace,label_ystart-(i+nlabels+nlabels_overlay)*label_yspace]), resources)
            resources = Ngl.Resources()
            resources.txFontHeightF = .02
            resources.txJust = "CenterLeft"
            pdashlabel = Ngl.add_text(wks,plot,dashlabels[i],labelstring_xstart,label_ystart-(i+nlabels+nlabels_overlay)*label_yspace,resources)

            
    if polygons:
        ### this is for making stacked polygons (as in for the soil carbon depth distributions)
        if len(x.shape) == 2:
            npoly_x = x.shape[0]
        else:
            npoly_x = 1
        if len(y.shape) == 2:
            npoly_y = y.shape[0]
        else:
            npoly_y = 1
        if npoly_x > 1 and npoly_y == 1:
            for i in range(npoly_x):
                polyres = Ngl.Resources()
                if colors != None:
                    polyres.gsFillColor = colors[i]
                if i == 0:
                    shape_x = np.concatenate((np.zeros(x.shape[1]), x[i,::-1]))
                else:
                    shape_x = np.concatenate((x[i-1,:], x[i,::-1]))
                shape_y = np.concatenate((y[:],y[::-1]))
                a = Ngl.add_polygon(wks,plot, shape_x, shape_y, polyres)
        else:
            raise NotImplementedError

    if type(shadederror_thickness) != type(None) or (type(shadederror_ulimit) != type(None) and type(shadederror_llimit) != type(None)):
        ### this is for surrounding each line with a shaded error area
        if type(shadederror_thickness) != type(None):
            if shadederror_thickness.shape != y.shape:
                raise RuntimeError
            symmetric = True
        else:
            if shadederror_ulimit.shape != y.shape or shadederror_llimit.shape != y.shape:
                raise RuntimeError
            symmetric = False           
        if len(y.shape) == 1:
            npoly = 1
        else:
            npoly = y.shape[0]
        shape_x = np.concatenate((x[:], x[::-1]))
        for i in range(npoly):
            polyres = Ngl.Resources()
            if shadederror_color != None:
                if type(shadederror_color) == type(0):
                    polyres.gsFillColor = shadederror_color                    
                    polyres.gsEdgeColor = shadederror_color
                else:                    
                    polyres.gsFillColor = shadederror_color[i]                    
                    polyres.gsEdgeColor = shadederror_color[i]
            else:
                if type(colors) != type(None):
                    polyres.gsFillColor = colors[i]
                    polyres.gsEdgeColor = colors[i]
            if shadederror_fillpattern != None:
                polyres.gsFillIndex = shadederror_fillpattern[i]
                polyres.gsEdgesOn = True
            if shadederror_opacity != None:
                polyres.gsFillOpacityF = shadederror_opacity
            if symmetric:
                if len(y.shape) == 1:
                    shape_y = np.concatenate((y[:]+shadederror_thickness[:],y[::-1]-shadederror_thickness[::-1]))
                else:
                    shape_y = np.concatenate((y[i,:]+shadederror_thickness[i,:],y[i,::-1]-shadederror_thickness[i,::-1]))
            else:
                if len(y.shape) == 1:
                    shape_y = np.concatenate((shadederror_ulimit[:],shadederror_llimit[::-1]))
                else:
                    shape_y = np.concatenate((shadederror_ulimit[i,:],shadederror_llimit[i,::-1]))                    
            a = Ngl.add_polygon(wks,plot, shape_x, shape_y, polyres)
            
    if shadederror_thickness_yindepvar != None:
        ### this is for surrounding each line with a shaded error area
        if shadederror_thickness_yindepvar.shape != x.shape:
            raise RuntimeError
        if len(x.shape) == 1:
            npoly = 1
        else:
            npoly = x.shape[0]
        shape_y = np.concatenate((y[:], y[::-1]))
        for i in range(npoly):
            polyres = Ngl.Resources()
            if shadederror_color != None:
                if type(shadederror_color) == type(0):
                    polyres.gsFillColor = shadederror_color
                else:                    
                    polyres.gsFillColor = shadederror_color[i]
            if shadederror_fillpattern != None:
                polyres.gsFillIndex = shadederror_fillpattern[i]
            if len(x.shape) == 1:
                shape_x = np.concatenate((x[:]+shadederror_thickness_yindepvar[:],x[::-1]-shadederror_thickness_yindepvar[::-1]))
            else:
                shape_x = np.concatenate((x[i,:]+shadederror_thickness_yindepvar[i,:],x[i,::-1]-shadederror_thickness_yindepvar[i,::-1]))
            a = Ngl.add_polygon(wks,plot, shape_x, shape_y, polyres)
            
    if type(overlay_shadederror_thickness) != type(None) or (type(overlay_shadederror_ulimit) != type(None) and type(overlay_shadederror_llimit) != type(None)):
        ### this is for surrounding each line with a shaded error area
        if type(shadederror_thickness) != type(None):
            if overlay_shadederror_thickness.shape != overlay_y.shape:
                raise RuntimeError
            symmetric = True
        else:
            if overlay_shadederror_ulimit.shape != overlay_y.shape or overlay_shadederror_llimit.shape != overlay_y.shape:
                raise RuntimeError
            symmetric = False                       
        if len(overlay_y.shape) == 1:
            npoly = 1
        else:
            npoly = overlay_y.shape[0]
        shape_x = np.concatenate((overlay_x[:], overlay_x[::-1]))
        for i in range(npoly):
            polyres = Ngl.Resources()
            if shadederror_color != None:
                if type(shadederror_color) == type(0) or type(shadederror_color) == type("") :
                    polyres.gsFillColor = shadederror_color
                else:                    
                    polyres.gsFillColor = shadederror_color[i]
            if shadederror_fillpattern != None:
                polyres.gsFillIndex = shadederror_fillpattern[i]
            if shadederror_opacity != None:
                polyres.gsFillOpacityF = shadederror_opacity
            if symmetric:
                if len(overlay_y.shape) == 1:
                    shape_y = np.concatenate((overlay_y[:]+overlay_shadederror_thickness[:],overlay_y[::-1]-overlay_shadederror_thickness[::-1]))
                else:
                    shape_y = np.concatenate((overlay_y[i,:]+overlay_shadederror_thickness[i,:],overlay_y[i,::-1]-overlay_shadederror_thickness[i,::-1]))
            else:
                if len(overlay_y.shape) == 1:
                    shape_y = np.concatenate((overlay_shadederror_ulimit[:],overlay_shadederror_llimit[::-1]))
                else:
                    shape_y = np.concatenate((overlay_shadederror_ulimit[i,:],overlay_shadederror_llimit[i,::-1]))
            a = Ngl.add_polygon(wks,plot, shape_x, shape_y, polyres)

    if box_whisker_plot:
        ## instead of plotting lines, plot box and whisker plots for the data instead
        ## two types possible: horizontal or vertical.  decide based on the shapes of the x and y terms; one must be 1-D and the other must be 2-D for this to make sense.
        from statslib import quartiles

        if len(x.shape) == 1 and len(y.shape) == 2:
            box_orientation = "vertical"
            nboxes = x.shape[0]
            if y.shape[1] != x.shape[0]:
                print("box_whisker_plot error: shapes don't match")
                raise RuntimeError 
            halfboxwith = 0.3 * (max(x) - min(x) ) / float(len(x))
        elif len(x.shape) == 2 and len(y.shape) == 1:
            box_orientation = "horizontal"
            nboxes = y.shape[0]
            if x.shape[1] != y.shape[0]:
                print("box_whisker_plot error: shapes don't match")
                raise RuntimeError 
            halfboxwith = 0.3 * (max(y) - min(y) ) / float(len(y))
        else:
            print('error xyplot box_whisker_plot: two types possible: horizontal or vertical.  decide based on the shapes of the x and y terms; one must be 1-D and the other must be 2-D for this to make sense.')
            raise RuntimeError

        boxres = Ngl.Resources()
        outlierdotres = Ngl.Resources()
        outlierdotres.gsMarkerIndex = 4
        outlierdotres.gsMarkerSizeF = dotsize
        mediandotres = Ngl.Resources()
        mediandotres.gsMarkerIndex = 16
        mediandotres.gsMarkerSizeF = dotsize
            

        for i in range(nboxes):
            if box_orientation == "vertical":
                if np.ma.count(y[:,i]) >= minobs_boxplot:
                    thequartiles = quartiles(y[:,i])
                    interq_r = thequartiles[2] - thequartiles[0]
                    adjacent_values = []
                    outlier_values = []
                    for j in range(len(y[:,i])):
                        if (thequartiles[0]-y[j,i] <= 1.5 * interq_r) and( y[j,i] - thequartiles[2] <= 1.5 * interq_r):
                            adjacent_values.append(y[j,i])
                        else:
                            if not y.mask[j,i]:
                                outlier_values.append(y[j,i])                    
                    thewhiskers = [np.min(adjacent_values), np.max(adjacent_values)]
                    box_x_indices = [x[i]-halfboxwith,x[i]+halfboxwith,x[i]+halfboxwith,x[i]-halfboxwith,x[i]-halfboxwith]
                    box_y_indices = [thequartiles[0], thequartiles[0], thequartiles[2], thequartiles[2], thequartiles[0]]
                    whisker_x_indices = [x[i], x[i]]
                    whisker1_y_indices = [thequartiles[0], thewhiskers[0]]
                    whisker2_y_indices = [thequartiles[2], thewhiskers[1]]
                    if colors != None:
                        boxres.gsLineColor = colors[i]
                        mediandotres.gsMarkerColor = colors[i]
                        outlierdotres.gsMarkerColor = colors[i]
                    a = Ngl.add_polyline(wks,plot, box_x_indices, box_y_indices, boxres)
                    b = Ngl.add_polyline(wks,plot, whisker_x_indices, whisker1_y_indices, boxres)
                    c = Ngl.add_polyline(wks,plot, whisker_x_indices, whisker2_y_indices, boxres)
                    pmarker = Ngl.add_polymarker(wks, plot, x[i], thequartiles[1], mediandotres)
                    if outlier_values != []:
                        for j in range(len(outlier_values)):
                                pmarker = Ngl.add_polymarker(wks, plot, x[i], outlier_values[j], outlierdotres)
            elif box_orientation == "horizontal":
                if np.ma.count(x[:,i]) >= minobs_boxplot:
                    thequartiles = quartiles(x[:,i])
                    interq_r = thequartiles[2] - thequartiles[0]
                    adjacent_values = []
                    outlier_values = []
                    for j in range(len(x[:,i])):
                        if (thequartiles[0]-x[j,i] <= 1.5 * interq_r) and( x[j,i] - thequartiles[2] <= 1.5 * interq_r):
                            adjacent_values.append(x[j,i])
                        else:
                            if not x.mask[j,i]:
                                outlier_values.append(x[j,i])                    
                    thewhiskers = [np.min(adjacent_values), np.max(adjacent_values)]
                    box_y_indices = [y[i]-halfboxwith,y[i]+halfboxwith,y[i]+halfboxwith,y[i]-halfboxwith,y[i]-halfboxwith]
                    box_x_indices = [thequartiles[0], thequartiles[0], thequartiles[2], thequartiles[2], thequartiles[0]]
                    whisker_y_indices = [y[i], y[i]]
                    whisker1_x_indices = [thequartiles[0], thewhiskers[0]]
                    whisker2_x_indices = [thequartiles[2], thewhiskers[1]]
                    a = Ngl.add_polyline(wks,plot, box_x_indices, box_y_indices, boxres)
                    b = Ngl.add_polyline(wks,plot, whisker1_x_indices, whisker_y_indices, boxres)
                    c = Ngl.add_polyline(wks,plot, whisker2_x_indices, whisker_y_indices, boxres)
                    pmarker = Ngl.add_polymarker(wks, plot, thequartiles[1], y[i], mediandotres)
                    if outlier_values != []:
                        for j in range(len(outlier_values)):
                            pmarker = Ngl.add_polymarker(wks, plot, outlier_values[j], y[i], outlierdotres)
            

    if stack_shade_values:
        ### instead of plotting lines, create shaded figures with the width of the shading equal to the data values.
        ### i.e. stack the lines onto each other, and represent the values with the shaded polygons rather than the line position.
        if len(x.shape) == 1 and len(y.shape) == 2:
            orientation = "vertical"
            npolygons = y.shape[0]
            nlevs = y.shape[1]
            if y.shape[1] != x.shape[0]:
                print("stack_shade_values error: shapes don't match")
                raise RuntimeError 
        elif len(x.shape) == 2 and len(y.shape) == 1:
            orientation = "horizontal"
            npolygons = x.shape[0]
            nlevs = x.shape[1]
            if x.shape[1] != y.shape[0]:
                print("stack_shade_values error: shapes don't match")
                raise RuntimeError 
        else:
            print('error xyplot stack_shade_values: two types possible: horizontal or vertical.  decide based on the shapes of the x and y terms; one must be 1-D and the other must be 2-D for this to make sense.')
            raise RuntimeError

        for i in range(npolygons):
            polyres = Ngl.Resources
            if not colors == None:
                polyres.gsFillColor = colors[i]
            if orientation == "horizontal":
                if i == 0:
                    lowerbound = np.zeros(nlevs)
                else:
                    lowerbound = x[0:i,:].sum(axis=0)
                upperbound = lowerbound + x[i,:]
                poly_x_indices = np.append(np.insert(np.concatenate([lowerbound, upperbound[::-1]]), 0, lowerbound[0]), upperbound[0])
                topy = y[0]-(y[1]-y[0])/2.
                poly_y_indices = np.append(np.insert(np.concatenate([y, y[::-1]]), 0, topy),topy)
                Ngl.add_polygon(wks,plot,poly_x_indices,poly_y_indices, polyres)
            elif orientation == "vertical":
                if i == 0:
                    lowerbound = np.zeros(nlevs)
                else:
                    lowerbound = y[0:i,:].sum(axis=0)
                upperbound = lowerbound + y[i,:]
                poly_y_indices = np.concatenate([lowerbound, upperbound[::-1]])
                poly_x_indices = np.concatenate([x, x[::-1]])
                Ngl.add_polygon(wks,plot,poly_x_indices,poly_y_indices, polyres)
                
    if hline != None:
        if type(hline) == float or type(hline) == int:
            hline_x = xrange
            hline_y = [hline,hline]
            hline_res = Ngl.Resources
            if hline_dashpattern != None:
                hline_res.gsLineDashPattern = hline_dashpattern
            if hline_color != None:
                hline_res.gsLineColor = hline_color
            line = Ngl.add_polyline(wks, plot, hline_x, hline_y, resources)
        else:
            for i in range(len(hline)):
                hline_x = xrange
                hline_y = [hline[i],hline[i]]        
                hline_res = Ngl.Resources
                if hline_dashpattern != None:
                    if type(hline_dashpattern) != float and type(hline_dashpattern) != int:
                        hline_res.gsLineDashPattern = hline_dashpattern[i]
                    else:
                        hline_res.gsLineDashPattern = hline_dashpattern
                if hline_color != None:
                    if type(hline_color) != float and type(hline_color) != int:
                        hline_res.gsLineColor = hline_color[i]
                    else:
                        hline_res.gsLineColor = hline_color
                line = Ngl.add_polyline(wks, plot, hline_x, hline_y, resources)

    if vline != None:
        if type(vline) == float or type(vline) == int:
            vline_y = yrange
            vline_x = [vline,vline]
            vline_res = Ngl.Resources
            if vline_dashpattern != None:
                vline_res.gsLineDashPattern = vline_dashpattern
            if vline_color != None:
                vline_res.gsLineColor = vline_color
            line = Ngl.add_polyline(wks, plot, vline_x, vline_y, resources)
        else:
            for i in range(len(vline)):
                vline_y = yrange
                vline_x = [vline[i],vline[i]]        
                vline_res = Ngl.Resources
                if vline_dashpattern != None:
                    if type(vline_dashpattern) != float and type(vline_dashpattern) != int:
                        vline_res.gsLineDashPattern = vline_dashpattern[i]
                    else:
                        vline_res.gsLineDashPattern = vline_dashpattern
                if vline_color != None:
                    if type(vline_color) != float and type(vline_color) != int:
                        vline_res.gsLineColor = vline_color[i]
                    else:
                        vline_res.gsLineColor = vline_color
                line = Ngl.add_polyline(wks, plot, vline_x, vline_y, resources)

    if vband != None:
        vband_res = Ngl.Resources()
        # vband_res.gsFillIndex = 17
        vband_res.gsFillColor = [0.85, 0.85, 0.85]
        zlx = [vband[0], vband[1], vband[1], vband[0], vband[0]]
        zly = [yrange[0], yrange[0], yrange[1], yrange[1], yrange[0]]
        Ngl.add_polygon(wks,plot, zlx, zly, vband_res)

    if hband != None:
        hband_res = Ngl.Resources()
        # hband_res.gsFillIndex = 17
        hband_res.gsFillColor = [0.85, 0.85, 0.85]        
        zly = [hband[0], hband[1], hband[1], hband[0], hband[0]]
        zlx = [xrange[0], xrange[0], xrange[1], xrange[1], xrange[0]]
        Ngl.add_polygon(wks,plot, zlx, zly, hband_res)


    if type(shaded_dot_data) != type(None):
        ## convert each data value into the index of the corresponding color bar.
        ## the way to do this is add up the number of levels that each index is greater than
        shaded_dot_data_flat = shaded_dot_data.flatten()
        marker_colorlevel = np.zeros(shaded_dot_data_flat.shape, dtype=np.int32)
        x_flat = x.flatten()
        y_flat = y.flatten()
        if (len(x_flat) != len(y_flat)) or (len(x_flat) != len(shaded_dot_data_flat)):
            raise RuntimeError
        ## make shared mask so that any masked values are skipped
        x_flat_mask = np.ma.masked_array(x_flat)
        y_flat_mask = np.ma.masked_array(y_flat)
        shaded_dot_data_flat_mask = np.ma.masked_array(shaded_dot_data_flat)
        combined_mask = (np.ma.getmaskarray(x_flat_mask) + np.ma.getmaskarray(y_flat_mask) + np.ma.getmaskarray(shaded_dot_data_flat_mask)) != 0
        if shuffle_shaded_dots:
            dotorder_shuffled = np.argsort(np.random.random(len(shaded_dot_data_flat)))
        for i in range(len(shaded_dot_data_flat)):
            if shuffle_shaded_dots:
                ii = dotorder_shuffled[i]
            else:
                ii = i   
            if not combined_mask[ii]:
                for j in range(len(shaded_dot_levels)):
                    if shaded_dot_data_flat[ii] > shaded_dot_levels[j]:
                        marker_colorlevel[ii] = marker_colorlevel[ii]+1
                resources = Ngl.Resources()
                resources.gsMarkerSizeF = dotsize / 2.
                resources.gsMarkerIndex = 16
                resources.gsMarkerColor = colorbars_int[marker_colorlevel[ii]]
                pmarker = Ngl.add_polymarker(wks, plot, x_flat[ii], y_flat[ii], resources)

    if type(shaded_line_data) != type(None):
        ## convert each data value into the index of the corresponding color bar.
        ## the way to do this is add up the number of levels that each index is greater than
        marker_colorlevel = np.zeros(shaded_line_data.shape, dtype=np.int32)
        ## assume x and y data arrive with the number of lines as the first dimension and the vertices of the line as the second dimension
        ## enforce for now that x and y have the same shape
        if x.shape != y.shape:
            raise RuntimeError
        if len(x[:,0]) != len(shaded_line_data):
            raise RuntimeError
        ## no masks for now...
        if shuffle_shaded_lines:
            lineorder_shuffled = np.argsort(np.random.random(len(shaded_line_data)))
        for i in range(len(shaded_line_data)):
            if shuffle_shaded_lines:
                ii = dotorder_shuffled[i]
            else:
                ii = i   
            for j in range(len(shaded_line_levels)):
                if shaded_line_data[ii] > shaded_line_levels[j]:
                    marker_colorlevel[ii] = marker_colorlevel[ii]+1
            resources = Ngl.Resources()
            resources.gsLineColor = colorbars_int[marker_colorlevel[ii]]
            resources.gsLineThicknessF = linethickness
            resources.gsLineOpacityF = line_opacity
            pmarker = Ngl.add_polyline(wks, plot, x[ii,:], y[ii,:], resources)


    if (type(overlay_vectors_x) != type(None)) and (type(overlay_vectors_y) != type(None)):
        # draw arrows on plot.  assume x and y arguments are nx2 arrays, with the first column being the arrow start and the second column being the arrow end
        if overlay_vectors_x.shape != overlay_vectors_y.shape:
            raise RuntimeError
        if len(overlay_vectors_x.shape) != 2:
            raise RuntimeError
        if overlay_vectors_x.shape[1] != 2:
            overlay_vectors_x = overlay_vectors_x.transpose
            overlay_vectors_y = overlay_vectors_y.transpose
            if overlay_vectors_x.shape[1] != 2:
                raise RuntimeError
        narrows = overlay_vectors_x.shape[0]
        if overlay_vectors_arrowheadlength == None:
            overlay_vectors_arrowheadlength = 0.1
            overlay_vectors_arrowheadwidth = 0.1
        for i in range(narrows):
            arrow_res = Ngl.Resources()
            arrow_res.gsLineThicknessF = overlay_vectors_thickness
            try:
                if overlay_vectors_forwards:
                    arrow_x, arrow_y = make_arrow(overlay_vectors_x[i,0], overlay_vectors_y[i,0], overlay_vectors_x[i,1], overlay_vectors_y[i,1], overlay_vectors_arrowheadlength, overlay_vectors_arrowheadwidth)
                else:
                    arrow_x, arrow_y = make_arrow(overlay_vectors_x[i,1], overlay_vectors_y[i,1], overlay_vectors_x[i,0], overlay_vectors_y[i,0], overlay_vectors_arrowheadlength, overlay_vectors_arrowheadwidth)
                if type(shaded_vectors_data) != type(None):
                    marker_colorlevel = 0
                    for level_j in range(len(shaded_vectors_levels)):
                         if shaded_vectors_data[i] > shaded_vectors_levels[level_j]:
                             marker_colorlevel = marker_colorlevel+1
                    arrow_res.gsLineColor = colorbars_int[marker_colorlevel]
                pline = Ngl.polyline(wks,plot,arrow_x,arrow_y, arrow_res)
            except:
                print(('had to skip an arrow: ', overlay_vectors_x[i,0], overlay_vectors_y[i,0], overlay_vectors_x[i,1], overlay_vectors_y[i,1]))

    if (type(overlay_ellipses_x) != type(None)) and (type(overlay_ellipses_y) != type(None)):
        # draw ellipses on plot.  
        if overlay_ellipses_x.shape != overlay_ellipses_y.shape:
            raise RuntimeError
        nellipses = len(overlay_ellipses_x)
        for i in range(nellipses):
            ellipse_res = Ngl.Resources()
            if overlay_ellipse_thickness != None:
                ellipse_res.gsLineThicknessF=overlay_ellipse_thickness
            # try:
            ellipse_x, ellipse_y = make_ellipse(overlay_ellipses_x[i], overlay_ellipses_y[i], overlay_ellipses_xaxis[i], overlay_ellipses_yaxis[i], angle=overlay_ellipses_angle[i], k=1)
            if not overlay_ellipses_filled:
                pline = Ngl.polyline(wks,plot,ellipse_x,ellipse_y, ellipse_res)
            else:
                if overlay_ellipses_opacity != None:
                    ellipse_res.gsFillOpacityF = overlay_ellipses_opacity
                    if overlay_ellipses_color == None:
                        ellipse_res.gsFillColor = "White"
                    else:
                        ellipse_res.gsFillColor = overlay_ellipses_color[i]
                    # ellipse_res_2 = Ngl.Resources()
                    # ellipse_res_2.gsFillOpacityF = .4
                    # ellipse_res_2.gsFillColor = "white"                
                    # pgon =  Ngl.polygon(wks,plot,ellipse_x,ellipse_y, ellipse_res_2)
                pgon =  Ngl.polygon(wks,plot,ellipse_x,ellipse_y, ellipse_res)
                pline = Ngl.polyline(wks,plot,ellipse_x,ellipse_y, ellipse_res)
            # except:
            #     print('had to skip an ellipse: ', overlay_ellipses_x[i], overlay_ellipses_y[i], overlay_ellipses_x[i], overlay_ellipses_y[i])


    if use_wks == None:
        Ngl.draw(plot)
        Ngl.frame(wks)
    
        if not file==None:
            Ngl.delete_wks(wks)
            #
            if makepng or showjupyter:
                pdf_to_png(file, density=png_dens)
            if jupyter_avail and showjupyter:
                print(' ')
                display(Image(file+'.png'))
        else:
            x11_window_list.append(wks)
    else:
        return plot




################################################################################
    
def plot_histogram(data_in, bins=10, file=None, therange=None, normed=False, weights_in=None, ytitle="", xtitle="", bar_width=1.0, yaxis_top=None, zeroline=False, maxlabels=10, label_binedges=True, writemean=False, axis=None, colors=None, colormap=None, thickness=2.5, labels=None, labelorder=None, label_xstart=None, label_ystart=None, label_yspace=None, aspect_ratio=None, meanline=False, histstyle="steps", ylabels=True, title=None, lineup_peakheights=False, hist_scales=None, labelsize=.02, cumulative=False, inverse_cumulative=False, flip_XY=False, yreverse=False, labelcolors=None, vlines=None, vlines_dashpattern=None, vband=None, return_histstats=False, inset_title=None, inset_title_x=None, inset_title_y=None, inset_title_fontsize=0.03, makepng=False, png_dens=pngdens, use_wks=None, showjupyter=False):  #scaled_cumulative_output=False

    ## takes as fundamental argument, data_in, either a single numpy array or a list of numpy arrays

    if showjupyter and type(file)==type(None):
        file = 'temp_fig_file'

    if use_wks == None:
        plot_type = get_workstation_type(file)
        
    if type(data_in) == type(np.arange(0)) or type(data_in) == type(np.ma.arange(0)):
        data_in_ndarray=True
    else:
        data_in_ndarray=False
        ### assume data_in is a list of arrays, then

    if data_in_ndarray:
        if therange==None:
            therange=np.array([np.ma.min(data_in),np.ma.max(data_in)])
        datadims = data_in.shape
        if axis != None:
            nplots = datadims[axis]
        else:
            nplots = 1
    else:
        nplots = len(data_in)
        if return_histstats:
            output_binedges=[]
            output_binfreq=[]


    FirstIteration = True

    for i in range(nplots):
        if data_in_ndarray:
            if axis == None:
                data_intermed = data_in[:]
            elif axis==0:
                data_intermed = data_in[i,:]
            elif axis == 1:
                data_intermed = data_in[:,i,:]
            if isinstance(data_intermed, np.ma.masked_array):
                ngood = np.ma.count(data_intermed)
                data = np.ma.getdata(data_intermed[np.logical_not(data_intermed.mask)])
            else:
                data = data_intermed[:]
        else:
            data_intermed = data_in[i]
            if isinstance(data_intermed, np.ma.masked_array):
                ngood = np.ma.count(data_intermed)
                data = np.ma.getdata(data_intermed[np.logical_not(data_intermed.mask)])
            else:
                data = data_intermed[:]

        if weights_in != None:
            if data_in_ndarray:
                if axis == None:
                    weights = weights_in[:]
                elif axis==0:
                    weights = weights_in[i,:]
                elif axis == 1:
                    weights = weights_in[:,i,:]
                if isinstance(data_intermed, np.ma.masked_array):
                    weights = np.ma.getdata(weights[np.logical_not(data_intermed.mask)])
            else:
                weights = weights_in[i]
                if isinstance(data_intermed, np.ma.masked_array):
                    weights = np.ma.getdata(weights[np.logical_not(data_intermed.mask)])
        else:
            weights = None
            

        data = np.ravel(data)
        ### first calculate histogram properties using the built-in numpy method
        hist_freq, bin_edges = np.histogram(data, bins=bins, range=therange, normed=normed, weights=weights)
        
        if cumulative:
            hist_freq = np.cumsum(np.array(hist_freq[:],dtype=np.float32))
            if normed: # or scaled_cumulative_output:
                hist_freq = hist_freq / hist_freq[len(hist_freq)-1]
            if inverse_cumulative:
                hist_freq = 1.-hist_freq
            #
            # if scaled_cumulative_output:
            #     hist_freq = hist_freq * weights.sum()

        # print(hist_freq)
        # print(bin_edges)
        # print(hist_freq.shape)
        # print(bin_edges.shape)
        
        if lineup_peakheights:
            hist_freq[:] = hist_freq[:] / hist_freq.max()

        if hist_scales != None:
            hist_freq[:] = hist_freq[:] * hist_scales[i]

        if return_histstats:
            if data_in_ndarray:
                output_binedges = bin_edges
                output_binfreq = hist_freq
            else:
                output_binedges.append(bin_edges)
                output_binfreq.append(hist_freq)

        nhist = bin_edges.size - 1
        dx = bin_edges[1:nhist+1]-bin_edges[0:nhist]
        bin_centers = bin_edges[0:nhist]+dx/2.

        if histstyle == "boxes":
            if not np.var(dx)/np.mean(dx) < .00001:
                raise RuntimeError('problem with assumption of uniform bin spacing')
            else:
                dxmean = dx[0]

        if FirstIteration:
            if use_wks == None:
                wks_res = Ngl.Resources()
                if file == None:
                    wks_res.wkPause = False
                else:
                    wks_res.wkPaperWidthF = page_width
                    wks_res.wkPaperHeightF = page_height
                    wks_res.wkOrientation = "portrait"
                    
                if not colormap == None:
                    colormap = parse_colormap(colormap)
                    wks_res.wkColorMap = colormap
                
                wks = Ngl.open_wks(plot_type,file,wks_res)
                if wks < 0 and plot_type == "x11":
                    clear_oldest_x11_window()
                    wks = Ngl.open_wks(plot_type,file,wks_res)
            else:
                wks = use_wks
            #
            hist_res = Ngl.Resources()
            hist_res.nglDraw = True
            hist_res.nglFrame = False


            if yaxis_top == None:
                max_y         = np.max(hist_freq)*1.25    # max value on y-axis
            else:
                max_y         = yaxis_top

            if not flip_XY:
                hist_res.tiXAxisString           = xtitle  # X axes label.
                hist_res.tiYAxisString           = ytitle  # Y axis label.
                if not ylabels:
                    hist_res.tmYLOn     = False
                    hist_res.tmYROn     = False
                # ------------- histogram resources ---------------------
                hist_res.trYMinF         = 0.0    # min value on y-axis
                if yaxis_top == None:
                    max_y         = np.max(hist_freq)*1.25    # max value on y-axis
                else:
                    max_y         = yaxis_top
                hist_res.trYMaxF  = max_y
                #
                hist_res.tmXBMode       = "Explicit"    # Define own tick mark labels.
                if maxlabels > 0:
                    if label_binedges:
                        if bin_edges.size <= maxlabels:
                            hist_res.tmXBValues     = bin_edges
                            hist_res.tmXBLabels     = bin_edges
                            hist_res.tmXBMinorOn    = False      # No minor tick marks.
                        else:
                            nskip = int(math.ceil(bin_edges.size / maxlabels))
                            hist_res.tmXBValues     = bin_edges[::nskip]
                            hist_res.tmXBLabels     = bin_edges[::nskip]
                            hist_res.tmXBMinorOn    = True      # No minor tick marks.
                            hist_res.tmXBMinorValues = bin_edges
                    else:
                        if bin_centers.size <= maxlabels:
                            hist_res.tmXBValues     = bin_centers
                            hist_res.tmXBLabels     = bin_centers
                            hist_res.tmXBMinorOn    = False      # No minor tick marks.
                        else:
                            nskip = int(math.ceil(bin_centers.size / maxlabels))
                            hist_res.tmXBValues     = bin_centers[::nskip]
                            hist_res.tmXBLabels     = bin_centers[::nskip]
                            hist_res.tmXBMinorOn    = True      # No minor tick marks.
                            hist_res.tmXBMinorValues = bin_centers
                else:
                    hist_res.tmXBLabelsOn    = False
                    hist_res.tmYLLabelsOn    = False
                #
                hist_res.tmXTOn         = False      # turn off the top tickmarks
                #
                # Make sure there's enough room for a bar at the first and last
                # X points of the data.
                #
                hist_res.trXMinF = min(bin_edges)
                hist_res.trXMaxF = max(bin_edges)
            else:                                                  ########### flip_XY = True
                hist_res.tiXAxisString           = ytitle  # X axes label.
                hist_res.tiYAxisString           = xtitle  # Y axis label.
                if not ylabels:
                    hist_res.tmXLOn     = False
                    hist_res.tmXROn     = False
                # ------------- histogram resources ---------------------
                hist_res.trXMinF         = 0.0    # min value on y-axis
                hist_res.trXMaxF  = max_y
                #
                hist_res.tmYBMode       = "Explicit"    # Define own tick mark labels.
                if label_binedges:
                    if bin_edges.size <= maxlabels:
                        hist_res.tmYBValues     = bin_edges
                        hist_res.tmYBLabels     = bin_edges
                        hist_res.tmYBMinorOn    = False      # No minor tick marks.
                    else:
                        nskip = int(math.ceil(bin_edges.size / maxlabels))
                        hist_res.tmYBValues     = bin_edges[::nskip]
                        hist_res.tmYBLabels     = bin_edges[::nskip]
                        hist_res.tmYBMinorOn    = True      # No minor tick marks.
                        hist_res.tmYBMinorValues = bin_edges
                else:
                    if bin_centers.size <= maxlabels:
                        hist_res.tmYBValues     = bin_centers
                        hist_res.tmYBLabels     = bin_centers
                        hist_res.tmYBMinorOn    = False      # No minor tick marks.
                    else:
                        nskip = int(math.ceil(bin_centers.size / maxlabels))
                        hist_res.tmYBValues     = bin_centers[::nskip]
                        hist_res.tmYBLabels     = bin_centers[::nskip]
                        hist_res.tmYBMinorOn    = True      # No minor tick marks.
                        hist_res.tmYBMinorValues = bin_centers
                #
                hist_res.tmYTOn         = False      # turn off the top tickmarks
                #
                # Make sure there's enough room for a bar at the first and last
                # X points of the data.
                #
                hist_res.trYMinF = min(bin_edges)
                hist_res.trYMaxF = max(bin_edges)
                #
                if yreverse:
                    hist_res.trYReverse   = True


            hist_res.tmXBMajorLengthF        = 0.01    # Force tickmarks to point
            hist_res.tmXBMajorOutwardLengthF = 0.01    # out by making the outward
            hist_res.tmXBMinorLengthF        = 0.005
            hist_res.tmXBMinorOutwardLengthF = 0.005
            hist_res.tmYLMajorLengthF        = 0.01    # tick length equal to the
            hist_res.tmYLMajorOutwardLengthF = 0.01    # total tick length
            hist_res.tmYLMinorLengthF        = 0.005
            hist_res.tmYLMinorOutwardLengthF = 0.005
            hist_res.tmXBLabelAngleF         = 90.  ## rotate x-axis labels
            hist_res.tmXBLabelJust     = "CenterRight"


            if aspect_ratio != None:
                if aspect_ratio > 1.:
                    hist_res.vpHeightF = 0.6 / aspect_ratio
                else:
                    hist_res.vpWidthF = 0.6 * aspect_ratio

            if title != None:
                hist_res.tiMainString = title

            #
            # Create dummy plot.
            #
            dummy = np.zeros(nhist-1)
            if not flip_XY:
                thehist  = Ngl.xy(wks,bin_centers,dummy,hist_res)
            else:
                thehist  = Ngl.xy(wks,dummy,bin_centers,hist_res)

            if zeroline:
                zeroline_res = Ngl.Resources()
                zeroline_res.gsLineDashPattern = 14
                zlx = [0., 0.]
                zly = [0., 2.*hist_res.trYMaxF]
                Ngl.add_polyline(wks,thehist, zlx, zly, zeroline_res)

            if type(vlines) != type(None):
                for line_i in range(len(vlines)):
                    vline_res = Ngl.Resources()
                    if vlines_dashpattern != None:
                        try:
                            vline_res.gsLineDashPattern = vlines_dashpattern[line_i]
                        except:
                            vline_res.gsLineDashPattern = vlines_dashpattern
                    zlx = [vlines[line_i], vlines[line_i]]
                    zly = [0., max_y]
                    if not flip_XY:
                        Ngl.add_polyline(wks,thehist, zlx, zly, vline_res)
                    else:
                        Ngl.add_polyline(wks,thehist, zly, zlx, vline_res)

            if vband != None:
                ### need to add grey to the current colormap
                Ngl.new_color(wks, 0.85, 0.85, 0.85)
                vband_res = Ngl.Resources()
                # vband_res.gsFillIndex = 17
                vband_res.gsFillColor = [0.85, 0.85, 0.85]
                zlx = [vband[0], vband[1], vband[1], vband[0], vband[0]]
                zly = [0., 0., max_y, max_y, 0.]
                if not flip_XY:
                    Ngl.add_polygon(wks,thehist, zlx, zly, vband_res)
                else:
                    Ngl.add_polygon(wks,thehist, zly, zlx, vband_res)


            if writemean:
                if axis == None:
                    if isinstance(data, np.ma.masked_array):
                        if weights_in == None:
                            datamean = np.ma.mean(data)
                        else:
                            datamean = np.ma.average(data, weights=weights)
                    else:
                        if weights_in == None:
                            datamean = np.mean(data)
                        else:
                            datamean = np.average(data, weights=weights)
                    meanstring = "Mean = %.2f" % datamean
                    meanstringres = Ngl.Resources()
                    meanstringres.txJust = "CenterLeft"
                    stringx = min(bin_edges)+0.1*(max(bin_edges)-min(bin_edges))
                    stringy = 0.9*hist_res.trYMaxF
                    if not flip_XY:
                        Ngl.add_text(wks, thehist, meanstring, stringx, stringy, meanstringres)
                    else:
                        Ngl.add_text(wks, thehist, meanstring, stringy, stringx, meanstringres)
                else:
                    raise NotImplementedError

            if not inset_title == None:
                if not flip_XY:
                    if inset_title_x == None:
                        inset_title_x = min(bin_edges) + (max(bin_edges)-min(bin_edges)) * 0.05
                    if inset_title_y == None:
                        inset_title_y = max_y * 0.05
                else:
                    if inset_title_y == None:
                        inset_title_y = min(bin_edges) + (max(bin_edges)-min(bin_edges)) * 0.05
                    if inset_title_x == None:
                        if yreverse:
                            inset_title_x = max_y * 0.95
                        else:
                            inset_title_x = max_y * 0.05
                resources = Ngl.Resources()
                resources.txFontHeightF = inset_title_fontsize
                resources.txJust = "CenterRight"
                Ngl.add_text(wks,thehist,inset_title,inset_title_x,inset_title_y,resources)
        
            if labels != None:
                ### expects labels to be a list of strings
                nlabels = len(labels)
                if labelorder == None:
                    labelorder = np.arange(nlabels)
                if not flip_XY:
                    if label_xstart == None:
                        label_xstart = min(bin_edges) + (max(bin_edges)-min(bin_edges)) * 0.65
                    if label_ystart == None:
                        label_ystart = max_y * 0.9
                    if label_yspace == None:
                        label_yspace =  max_y * 0.075
                else:
                    if label_xstart == None:
                        label_xstart = max_y * 0.65
                    if not yreverse:
                        if label_ystart == None:
                            label_ystart = min(bin_edges) + (max(bin_edges)-min(bin_edges)) * 0.7
                        if label_yspace == None:
                            label_yspace =  (max(bin_edges)-min(bin_edges)) * 0.075                    
                    else:
                        if label_ystart == None:
                            label_ystart = min(bin_edges) + (max(bin_edges)-min(bin_edges)) * 0.1
                        if label_yspace == None:
                            label_yspace =  - (max(bin_edges)-min(bin_edges)) * 0.075                    
                resources = Ngl.Resources()
                resources.txFontHeightF = labelsize
                resources.txJust = "CenterLeft"
                for j in range(nlabels):
                    if labelcolors != None:
                        if labelcolors[j] >= 0:
                            resources.txFontColor = labelcolors[j]
                    elif colors != None:
                        if colors[j] >= 0:
                            resources.txFontColor = colors[j]
                    pstring = Ngl.add_text(wks,thehist,labels[j],label_xstart,label_ystart-labelorder[j]*label_yspace,resources)


            FirstIteration = False

        #
        # Get indices where rain data is above zero. Draw filled bars for each
        # of these points.
        #
        above_zero     = np.greater(hist_freq,0.0)
        ind_above_zero = np.nonzero(above_zero)  # We know that the values are 
                                                      # above zero.
        num_above = len(ind_above_zero[0])

        #
        # Create resource list for polygons.
        #
        pgres             = Ngl.Resources()
        if colors != None:
            pgres.gsLineColor = colors[i]
            pgres.gsLineThicknessF = thickness
                
        if histstyle == "boxes":
            #
            # Create arrays to hold polygon points. Since we are drawing a rectangle,
            # we just need 5 points for the filled rectangle, and we can use the
            # first four points of each for the outline.
            #
            px = np.zeros(5*num_above,bin_centers.dtype.char)
            py = np.zeros(5*num_above,hist_freq.dtype.char)

            bin_centers_above_zero = np.take(bin_centers,ind_above_zero)
            px[0::5] = (bin_centers_above_zero - bar_width*dxmean/2.).astype(bin_centers.dtype.char)
            px[1::5] = (bin_centers_above_zero - bar_width*dxmean/2.).astype(bin_centers.dtype.char)
            px[2::5] = (bin_centers_above_zero + bar_width*dxmean/2.).astype(bin_centers.dtype.char)
            px[3::5] = (bin_centers_above_zero + bar_width*dxmean/2.).astype(bin_centers.dtype.char)
            px[4::5] = (bin_centers_above_zero - bar_width*dxmean/2.).astype(bin_centers.dtype.char)
            py[0::5] = hist_res.trYMinF
            py[1::5] = np.take(hist_freq,ind_above_zero)
            py[2::5] = np.take(hist_freq,ind_above_zero)
            py[3::5] = hist_res.trYMinF
            py[4::5] = hist_res.trYMinF
            
            #
            # For the outlines, we don't need the fifth point.
            #
            if not flip_XY:
                polyl    = Ngl.add_polyline(wks,thehist,px,py,pgres)
            else:
                polyl    = Ngl.add_polyline(wks,thehist,py,px,pgres)

        elif histstyle == "steps":
            finished_histogram = False
            j = 0
            while not finished_histogram:
                px = []
                py = []
                if hist_freq[j] > 0. and not finished_histogram and j != 0:
                    j = j+1
                    if j >= nhist:
                        finished_histogram = True
                px.extend([bin_edges[j]])
                py.extend([0.])
                finished_block = False
                while not finished_block:
                    px.extend([bin_edges[j], bin_edges[j+1]])
                    py.extend([hist_freq[j], hist_freq[j]])
                    if j == nhist - 1:
                        finished_block = True
                        finished_histogram = True
                    else:
                        if hist_freq[j+1] > 0.:
                            j = j+1
                        else:
                            finished_block = True
                px.extend([bin_edges[j+1]])
                py.extend([0.])
                if not flip_XY:
                    polyl    = Ngl.add_polyline(wks,thehist,px,py,pgres)
                else:
                    polyl    = Ngl.add_polyline(wks,thehist,py,px,pgres)
                j = j+1
                        
        

        if meanline:
            meanline_res             = Ngl.Resources()
            if colors != None:
                meanline_res.gsLineColor = colors[i]
            meanline_res.gsLineThicknessF = thickness
            meanline_res.gsLineDashPattern = 14
            if isinstance(data, np.ma.masked_array):
                if weights_in == None:
                    datamean = np.ma.mean(data)
                else:
                    datamean = np.ma.average(data, weights=weights)
            else:
                if weights_in == None:
                    datamean = np.mean(data)
                else:
                    datamean = np.average(data, weights=weights)
            zlx = [datamean, datamean]
            zly = [0., 2.*hist_res.trYMaxF]
            if not flip_XY:
                Ngl.add_polyline(wks,thehist, zlx, zly, meanline_res)
            else:
                Ngl.add_polyline(wks,thehist, zly, zlx, meanline_res)             

    if use_wks == None:
        Ngl.draw(thehist)
        
        
        if not file==None:
            #
            if return_histstats:
                Ngl.delete_wks(wks)
                if makepng or showjupyter:
                    pdf_to_png(file, density=png_dens)
                if jupyter_avail and showjupyter:
                    print(' ')
                    display(Image(file+'.png'))
                return output_binedges, output_binfreq
            else:   
                Ngl.delete_wks(wks)
                if makepng or showjupyter:
                    pdf_to_png(file, density=png_dens)
                if jupyter_avail and showjupyter:
                    print(' ')
                    display(Image(file+'.png'))
            #
        else:
            x11_window_list.append(wks)
            if return_histstats:
                return output_binedges, output_binfreq
    else:
        return thehist



################
def fill_nomap(data, x, y, contour_fill=False, contour=False, levels=None, file=None, title=None, subtitle=None, aspect_ratio=None, overlay_contour_data=None, overlay_contour_levels=None, xrange=None, yrange=None, xlog=False, ylog=False, yreverse=False, linelabels=False,ytitle=None, xtitle=None, pixels=False, colormap=None, reverse_colors=False, expand_colormap_middle=None, overlay_x=None, overlay_y=None, overlay_dots=False, overlay_color=None, overlay_linethickness=2.5, overlay_dashpattern=None, overlay_color_list=None, makepng=False, png_dens=pngdens, showjupyter=False):
    IM = x.shape[0]
    JM = y.shape[0]
    data = np.squeeze(data[:])

    # if data.shape != (JM,IM):
    #     raise SizeMismatchError

    if showjupyter and type(file)==type(None):
        file = 'temp_fig_file'

    plot_type = get_workstation_type(file)


    wks_res = Ngl.Resources()

    if file == None:
        wks_res.wkPause = True
    else:
        wks_res.wkPaperWidthF = page_width
        wks_res.wkPaperHeightF = page_height
        wks_res.wkOrientation = "portrait"


    resources = Ngl.Resources()
    resources.cnFillOn          = True
    resources.cnLinesOn         = contour
    
    if pixels:
        resources.cnFillMode        = "RasterFill"
        resources.cnLinesOn         = contour
        resources.cnLineLabelsOn    = False
        resources.cnRasterSmoothingOn = contour_fill


    resources.nglDraw = False
    resources.nglFrame = False


    #     if added_cyclic:
    #         resources.sfXArray        = lon[0:IM-1]
    #         resources.sfXCStartV = np.float(np.min(lon[0:IM-1]))
    #         resources.sfXCEndV   = np.float(np.max(lon[0:IM-1]))
    #     else:

    resources.sfXArray        = x[:]
    # resources.sfXCStartV = np.float(np.min(x))
    # resources.sfXCEndV   = np.float(np.max(x))

    resources.sfYArray        = y[:]
    # resources.sfYCStartV = np.float(np.min(y))
    # resources.sfYCEndV   = np.float(np.max(y))

    if yrange != None:
        resources.trYMinF = np.min(yrange)
        resources.trYMaxF = np.max(yrange)
    else:
        if not ylog:
            yrange = [np.ma.min(y), np.ma.max(y)]
        
    if xrange != None:
        resources.trXMinF = np.min(xrange)
        resources.trXMaxF = np.max(xrange)
    else:
        if not xlog:
            xrange = [np.ma.min(x), np.ma.max(x)]


    if ylog:
        resources.nglYAxisType = "LogAxis"
    else:
        resources.nglYAxisType = "LinearAxis"

    if xlog:
        resources.nglXAxisType = "LogAxis"
    else:
        resources.nglXAxisType = "LinearAxis"


    resources.cnLineLabelsOn            = linelabels
    
    if yreverse:
        resources.trYReverse   = True
    
    resources.lbOrientation         = "horizontal"
    resources.lbPerimThicknessF     = 2.
    resources.lbTitleFontThicknessF = 2.
    resources.lbLabelStride         = 1
    resources.lbRightMarginF        = 0.15
    resources.lbLeftMarginF         = 0.15
    resources.lbTopMarginF           = 0.
    resources.lbBottomMarginF        = 0.5
    resources.lbLabelFontHeightF     = 0.02

    if xtitle != None:
        resources.tiXAxisString           = xtitle  # X axis label.
    if ytitle != None:
        resources.tiYAxisString           = ytitle  # Y axis label.

    if type(levels) == type(None):
        resources.cnMaxLevelCount      = 15
    else:
        resources.cnLevelSelectionMode      = 'ExplicitLevels'
        resources.cnLevels = levels


    if title != None:
        resources.tiMainString = title
        
    if subtitle != None:
        resources.lbTitleString = subtitle

    if aspect_ratio != None:
        if aspect_ratio > 1.:
            resources.vpHeightF =  0.6  / aspect_ratio
        else:
            resources.vpWidthF =  0.6  * aspect_ratio

    wks = Ngl.open_wks(plot_type,file,wks_res)
    if wks < 0 and plot_type == "x11":
        clear_oldest_x11_window()
        wks = Ngl.open_wks(plot_type,file,wks_res)

    if colormap != None:
        colormap = parse_colormap(colormap)
        Ngl.define_colormap(wks, colormap)

    if expand_colormap_middle != None:
        cmap = Ngl.get_MDfloat_array(wks, "wkColorMap")
        cmap_length_old = cmap.shape[0]
        center = (cmap_length_old - 1 ) / 2 + 1
        cmap_length_new = cmap_length_old + expand_colormap_middle - 1
        cmap_new = np.zeros([cmap_length_new, 3])
        cmap_new[0:center,:] = cmap[0:center,:]
        cmap_new[center:center+expand_colormap_middle,:] = cmap[center,:]
        cmap_new[center+expand_colormap_middle:cmap_length_new,:] = cmap[center+1:cmap_length_old,:]
        rlist = Ngl.Resources()
        rlist.wkColorMap = cmap_new
        Ngl.set_values(wks,rlist)

    if reverse_colors:
        resources.nglSpreadColorStart = -1
        resources.nglSpreadColorEnd = 2

    plot = Ngl.contour(wks,data,resources)

    if overlay_contour_data != None:
        resources = Ngl.Resources()
        resources.sfXArray        = x[:]
        resources.sfYArray        = y[:]

        resources.nglDraw = False
        resources.nglFrame = False

        if yrange != None:
            resources.trYMinF = np.min(yrange)
            resources.trYMaxF = np.max(yrange)
        else:
            if not ylog:
                yrange = [np.ma.min(y), np.ma.max(y)]

        if xrange != None:
            resources.trXMinF = np.min(xrange)
            resources.trXMaxF = np.max(xrange)
        else:
            if not xlog:
                xrange = [np.ma.min(x), np.ma.max(x)]

        resources.nglYAxisType = "LinearAxis"

        if yreverse:
            resources.trYReverse   = True

        if overlay_contour_levels != None:
            resources.cnLevelSelectionMode      = 'ExplicitLevels'
            resources.cnLevels = overlay_contour_levels

        resources.cnLineLabelsOn            = linelabels
        
        resources.cnFillOn          = False
        resources.cnLineThicknessF  = 3.0

        if type(overlay_contour_data) != type([]):
            contour_overlay = Ngl.contour(wks, overlay_contour_data, resources)
            Ngl.overlay(plot,contour_overlay)
        else:
            for list_i in range(len(overlay_contour_data)):
                if overlay_color_list != None:
                    resources.cnLineColor = overlay_color_list[list_i]
                contour_overlay = Ngl.contour(wks, overlay_contour_data[list_i], resources)        
                Ngl.overlay(plot,contour_overlay)
                    


    if not (type(overlay_x)==type(None) and type(overlay_y)==type(None)):
        ### overlay line(s) on top. if more than one line, have shape of [a,b]
        ### where a is the number of lines and b is the number of points in each line
        try:
            ndims_overlay_y = np.size(overlay_y.shape)
        except AttributeError:
            ## handle case if overlay_y is a list.  assume it is a 2-d list
            if isinstance(overlay_y, list):
                if type(overlay_y[0]) == list:
                    ndims_overlay_y = 2
                else:
                    ndims_overlay_y = 1
            else:
                raise RuntimeError
        try:
            ndims_overlay_x = np.size(overlay_x.shape)
        except AttributeError:
            ## handle case if overlay_x is a list.  assume it is a 2-d list
            if isinstance(overlay_x, list):
                if type(overlay_x[0]) == list:
                    ndims_overlay_x = 2
                else:
                    ndims_overlay_x = 1
            else:
                raise RuntimeError
        if ndims_overlay_y == 1:
            resources = Ngl.Resources()
            if overlay_dots:
                # resources.gsMarkLineMode = 'Markers'
                # resources.gsMarker = 1
                resources.gsMarkerIndex = 1
                resources.gsMarkerSizeF = dotsize * 1.5
                # resources.gsMarkerThicknessF = overlay_linethickness
                if overlay_color != None:
                    resources.gsMarkerColor = overlay_color
            else:
                resources.gsLineThicknessF = overlay_linethickness
            if overlay_color != None:
                resources.gsLineColor = overlay_color
            if overlay_dashpattern != None:
                resources.gsLineDashPattern = overlay_dashpattern
            ### need to manually handle masked values since add_polyline doesn't seem to do that
            if isinstance(overlay_y, np.ndarray) and isinstance(overlay_x, np.ndarray):
                polyline_x, polyline_y = handle_masks(overlay_x, overlay_y)
            elif isinstance(overlay_y, list) and isinstance(overlay_x, list):
                maskedarray_overlayx = Nonemask(overlay_x)
                maskedarray_overlayy = Nonemask(overlay_y)
                polyline_x, polyline_y = handle_masks(maskedarray_overlayx, maskedarray_overlayy)
            else:
                raise RuntimeError
            if overlay_dots:
                pline = Ngl.add_polymarker(wks, plot, polyline_x, polyline_y, resources)
            else:
                pline = Ngl.add_polyline(wks, plot, polyline_x, polyline_y, resources)
        elif ndims_overlay_y == 2 and ndims_overlay_x == 1:
            shape_overlay_y = overlay_y.shape
            #          pline = np.zeros(shape_overlay_x[0])
            for i in range(shape_overlay_y[0]):
                resources = Ngl.Resources()
                if overlay_dots:
                    # resources.gsMarkLineMode = 'Markers'
                    # resources.gsMarker = 1
                    resources.gsMarkerIndex = 1
                    resources.gsMarkerSizeF = dotsize * 1.5
                else:
                    resources.gsLineThicknessF = overlay_linethickness
                if overlay_color != None:
                    if type(overlay_color) == int or type(overlay_color) == type('a string'):
                        if overlay_color >= 0 or type(overlay_color) == type('a string'):
                            if overlay_dots:
                                resources.gsMarkerColor = overlay_color
                            else:
                                resources.gsLineColor = overlay_color
                    else:
                        if overlay_color[i] >= 0:
                            resources.gsLineColor = overlay_color[i]
                if overlay_dashpattern != None:
                    resources.gsLineDashPattern = overlay_dashpattern[i]
                ### need to manually handle masked values since add_polyline doesn't seem to do that
                polyline_x, polyline_y = handle_masks(overlay_x, overlay_y[i,:])
                if overlay_dots:
                    pline = Ngl.add_polymarker(wks, plot, polyline_x, polyline_y, resources)
                else:
                    pline = Ngl.add_polyline(wks, plot, polyline_x, polyline_y, resources)
        elif ndims_overlay_y == 2 and ndims_overlay_x == 2:
            # assume each point has its own coordinate
            if isinstance(overlay_y, np.ndarray) and isinstance(overlay_x, np.ndarray):
                shape_overlay_y = overlay_y.shape
                shape_overlay_x = overlay_x.shape
                if shape_overlay_y != shape_overlay_x:
                    raise RuntimeError
                nlines = shape_overlay_y[0]
                overlaydata_list = False
            elif isinstance(overlay_y, list) and isinstance(overlay_x, list):
                if len(overlay_y) != len(overlay_x):
                    raise RuntimeError
                nlines = len(overlay_y)
                overlaydata_list = True
            else:
                raise RuntimeError
            #
            for i in range(nlines):
                resources = Ngl.Resources()
                if overlay_dots:
                    # resources.gsMarkLineMode = 'Markers'
                    # resources.gsMarker = 1
                    resources.gsMarkerIndex = 1
                    resources.gsMarkerSizeF = dotsize * 1.5
                else:
                    resources.gsLineThicknessF = overlay_linethickness
                if overlay_color != None:
                    if type(overlay_color) == int or type(overlay_color) == type("string"):
                        if overlay_color >= 0:
                            resources.gsLineColor = overlay_color
                    else:
                        if overlay_color[i] >= 0:
                            resources.gsLineColor = overlay_color[i]
                if overlay_dashpattern != None:
                    resources.gsLineDashPattern = overlay_dashpattern[i]
                ### need to manually handle masked values since add_polyline doesn't seem to do that
                if not overlaydata_list:
                    polyline_x, polyline_y = handle_masks(overlay_x[i,:], overlay_y[i,:])
                else:
                    maskedarray_overlayx = Nonemask(overlay_x[i])
                    maskedarray_overlayy = Nonemask(overlay_y[i])
                    polyline_x, polyline_y = handle_masks(maskedarray_overlayx, maskedarray_overlayy)
                if overlay_dots:
                    pline = Ngl.add_polymarker(wks, plot, polyline_x, polyline_y, resources)
                else:
                    pline = Ngl.add_polyline(wks, plot, polyline_x, polyline_y, resources)

        else:
            raise NotImplementedError
        
        
    Ngl.draw(plot)



    if not file==None:
        Ngl.delete_wks(wks)
        #
        if makepng or showjupyter:
            pdf_to_png(file, density=png_dens)
        if jupyter_avail and showjupyter:
            print(' ')
            display(Image(file+'.png'))
    else:
        x11_window_list.append(wks)

################################################################################
    
def map_stationmarkers(lat, lon, data=None, polar=None, projection="CylindricalEquidistant", file=None, title=None, subtitle=None, aspect_ratio=None, latlimits=None, lonlimits=None, grid=True, marker_colors=None, colormap="wh-bl-gr-ye-re", levels=None, nlevels=None, markershape="circle_filled", markersize=0.03, markerthickness=1.0, latcenter=None, loncenter=None, specialprojection=None, nomaplimits=False, inset_title=None, inset_title_x=None, inset_title_y=None, inset_title_y_list=None, inset_title_x_list=None, inset_title_colors=None, inset_title_yspace=None, inset_title_fontsize=0.025, makepng=False, png_dens=pngdens):

    plot_type = get_workstation_type(file)

    wks_res = Ngl.Resources()

    if colormap != None:
        colormap = parse_colormap(colormap)
        wks_res.wkColorMap = colormap

    if file == None:
        wks_res.wkPause = True
    else:
        wks_res.wkPaperWidthF = page_width
        wks_res.wkPaperHeightF = page_height
        wks_res.wkOrientation = "portrait"

    resources = Ngl.Resources()

    map_proj_setup(resources, lon=lon, lat=lat, polar=polar, projection=projection, latlimits=latlimits, lonlimits=lonlimits, nomaplimits=nomaplimits, latcenter=latcenter, loncenter=loncenter, grid=grid, specialprojection=specialprojection)
   
    resources.lbOrientation         = "horizontal"
    resources.lbPerimThicknessF     = 2.
    resources.lbTitleFontThicknessF = 1.5
    resources.lbLabelStride         = 1
    resources.lbRightMarginF        = 0.15
    resources.lbLeftMarginF         = 0.15
    resources.lbTopMarginF           = 0.
    resources.lbBottomMarginF        = 0.5
    resources.lbLabelFontHeightF     = 0.02

    resources.nglFrame = False
    resources.nglDraw = True

    if title != None:
        resources.tiMainString = title
        
    if subtitle != None:
        resources.lbTitleString = subtitle
        resources.lbTitleFontHeightF = 0.02

    if aspect_ratio != None:
        if aspect_ratio > 1.:
            resources.vpHeightF =  0.6  / aspect_ratio
        else:
            resources.vpWidthF =  0.6  * aspect_ratio

    wks = Ngl.open_wks(plot_type,file,wks_res)
    if wks < 0 and plot_type == "x11":
        clear_oldest_x11_window()
        wks = Ngl.open_wks(plot_type,file,wks_res)

    if type(data) == type(None):
        # here I manually color each symbol a given color
        plot = Ngl.map(wks,resources)
        resources = Ngl.Resources()
        resources.gsMarkerSizeF = markersize
        resources.gsMarkerThicknessF  = markerthickness
        resources.gsMarkerIndex = markershape

        if len(lat.shape) > 1:
            ngroups = lat.shape[0]
            two_d = True
        else:
            ngroups = 1
            two_d = False

        for i in range(ngroups):
            if two_d:
                if marker_colors != None:
                    resources.gsMarkerColor = marker_colors[i]
                pmarker = Ngl.add_polymarker(wks, plot, lon[i,:], lat[i,:], resources)
            else:
                if marker_colors != None:
                    resources.gsMarkerColor = marker_colors
            pmarker = Ngl.add_polymarker(wks, plot, lon, lat, resources)

    else:
        # here I want the color to correspond to a given value on a colorbar
        # assume smallest colorbar color = 2
        dummylats = np.arange(-99,-98.9, .01)
        dummylons = np.arange(-179,-178.9, .01)
        dummy_data = np.random.rand(10,10)
        resources.sfXArray = dummylons
        resources.sfYArray = dummylats
        resources.cnNoDataLabelOn = False
        if type(levels) == type(None):
            if nlevels == None:
                nlevels=15
            levels = np.arange(nlevels) * (data.max()-data.min()) / (nlevels-1.) + data.min()
        else:
            nlevels = len(levels)
        resources.cnFillOn          = True
        resources.cnLinesOn         = True
        resources.cnLevelSelectionMode      = 'ExplicitLevels'
        resources.cnLevels = levels
        cmap = Ngl.retrieve_colormap(wks)
        nbars = nlevels+1
        colorbars = np.arange(nbars) / (nbars-1.) * (cmap.shape[0]-3)
        colorbars_int = np.array(colorbars+2., dtype=np.int32)
        resources.cnFillColors = colorbars_int
        plot = Ngl.contour_map(wks,dummy_data,resources)

        ## next convert each data value into the index of the corresponding color bar.
        ## the way to do this is add up the number of levels that each index is greater than
        marker_colorlevel = np.zeros(data.shape, dtype=np.int32)
        for i in range(len(data)):
            try:
                unmasked = type(data[i]) != type(np.ma.masked_array()) and type(data[i]) != np.ma.core.MaskedConstant
            except:
                unmasked = type(data[i]) != type(np.ma.masked_array())
            if unmasked:
                for j in range(len(levels)):
                    if data[i] > levels[j]:
                        marker_colorlevel[i] = marker_colorlevel[i]+1
                resources = Ngl.Resources()
                resources.gsMarkerSizeF = markersize
                resources.gsMarkerThicknessF  = markerthickness
                resources.gsMarkerIndex = markershape
                resources.gsMarkerColor = colorbars_int[marker_colorlevel[i]]
                pmarker = Ngl.add_polymarker(wks, plot, lon[i], lat[i], resources)
                if markershape == "circle_filled":
                    resources = Ngl.Resources()
                    resources.gsMarkerSizeF = markersize
                    resources.gsMarkerThicknessF  = markerthickness
                    resources.gsMarkerIndex = "hollow_circle"
                    pmarker = Ngl.add_polymarker(wks, plot, lon[i], lat[i], resources)
                

    if inset_title != None:
        if type(inset_title) == type(""):
            inset_title_res = Ngl.Resources()
            inset_title_res.txFontHeightF  = inset_title_fontsize
            inset_title_res.txJust  = "CenterLeft"
            txt = Ngl.add_text(wks,plot,inset_title,inset_title_x, inset_title_y,inset_title_res)
        elif type(inset_title) == type([]):
            for inset_title_i in range(len(inset_title)):
                inset_title_res = Ngl.Resources()
                inset_title_res.txFontHeightF  = inset_title_fontsize
                if inset_title_colors != None:
                    inset_title_res.txFontColor = inset_title_colors[inset_title_i]
                if inset_title_y_list == None:
                    inset_title_y_element = inset_title_y + inset_title_yspace*inset_title_i
                else:
                    inset_title_y_element = inset_title_y_list[inset_title_i]
                if inset_title_x_list == None:
                    inset_title_x_element = inset_title_x
                else:
                    inset_title_x_element = inset_title_x_list[inset_title_i]
                txt = Ngl.add_text(wks,plot,inset_title[inset_title_i],inset_title_x_element, inset_title_y_element, inset_title_res)            


    Ngl.draw(plot) 

    if not file==None:
        Ngl.delete_wks(wks)
        #
        if makepng:
            pdf_to_png(file, density=png_dens)
    else:
        x11_window_list.append(wks)


################################################################################
def map_changevectors(delta_lat, delta_lon, lat, lon, polar=None, projection="CylindricalEquidistant", file=None, title=None, subtitle=None, aspect_ratio=None, latlimits=None, lonlimits=None, grid=True, colormap=None, vectorthickness=None, arrowheadlength=1.5, arrowheadwidth=1.5, latcenter=None, loncenter=None, specialprojection=None, nomaplimits=False, greatcircle=True, arrowsforwards=True, vector_colors=None, vector_color_levels=None, vector_color_nlevels=None, overlay_contour_data=None, overlay_contour_levels=None, overlay_contour_lat=None, overlay_contour_lon=None, overlay_contour_colors=None, overlay_contour_thickness=None, makepng=False, png_dens=pngdens):
        
    plot_type = get_workstation_type(file)

    wks_res = Ngl.Resources()

    if colormap != None:
        colormap = parse_colormap(colormap)
        wks_res.wkColorMap = colormap

    if file == None:
        wks_res.wkPause = True
    else:
        wks_res.wkPaperWidthF = page_width
        wks_res.wkPaperHeightF = page_height
        wks_res.wkOrientation = "portrait"

    resources = Ngl.Resources()

    map_proj_setup(resources, lon=lon, lat=lat, polar=polar, projection=projection, latlimits=latlimits, lonlimits=lonlimits, nomaplimits=nomaplimits, latcenter=latcenter, loncenter=loncenter, grid=grid, specialprojection=specialprojection)

    resources.lbOrientation         = "horizontal"
    resources.lbPerimThicknessF     = 2.
    resources.lbTitleFontThicknessF = 1.5
    resources.lbLabelStride         = 1
    resources.lbRightMarginF        = 0.15
    resources.lbLeftMarginF         = 0.15
    resources.lbTopMarginF           = 0.
    resources.lbBottomMarginF        = 0.5
    resources.lbLabelFontHeightF     = 0.02

    resources.nglFrame = False
    resources.nglDraw = True

    if title != None:
        resources.tiMainString = title
        
    if subtitle != None:
        resources.lbTitleString = subtitle
        resources.lbTitleFontHeightF = 0.02

    if aspect_ratio != None:
        if aspect_ratio > 1.:
            resources.vpHeightF =  0.6  / aspect_ratio
        else:
            resources.vpWidthF =  0.6  * aspect_ratio

    wks = Ngl.open_wks(plot_type,file,wks_res)
    if wks < 0 and plot_type == "x11":
        clear_oldest_x11_window()
        wks = Ngl.open_wks(plot_type,file,wks_res)


    if vector_colors != None:
        ### make a color bar, both graphically and as a vector
        if vector_color_levels == None:
           vector_color_levels = np.arange(vector_colors.min(), vector_colors.max(),  (vector_colors.max()- vector_colors.min())/11.)

        # here I want the color to correspond to a given value on a colorbar
        # assume smallest colorbar color = 2
        dummylats = np.arange(-99,-98.9, .01)
        dummylons = np.arange(-179,-178.9, .01)
        dummy_data = np.random.rand(10,10)
        resources.sfXArray = dummylons
        resources.sfYArray = dummylats
        resources.cnNoDataLabelOn = False
        if vector_color_levels == None:
            if vector_color_nlevels == None:
                vector_color_nlevels=15
            vector_color_levels = np.arange(vector_color_nlevels) * (vector_colors.max()-vector_colors.min()) / (vector_color_nlevels-1.) + vector_colors.min()
        else:
            vector_color_nlevels = len(vector_color_levels)
        resources.cnFillOn          = True
        resources.cnLinesOn         = True
        resources.cnLevelSelectionMode      = 'ExplicitLevels'
        resources.cnLevels = vector_color_levels
        cmap = Ngl.retrieve_colormap(wks)
        nbars = vector_color_nlevels+1
        colorbars = np.arange(nbars) / (nbars-1.) * (cmap.shape[0]-3)
        colorbars_int = np.array(colorbars+2., dtype=np.int32)
        resources.cnFillColors = colorbars_int
        plot = Ngl.contour_map(wks,dummy_data,resources)
        marker_colorlevel = np.zeros(vector_colors.shape, dtype=np.int32)
    else:
        plot = Ngl.map(wks,resources)


    ## overlay_contours
    if overlay_contour_data != None:

        # 
        # Copy just the contour resources from mpres to a new resource list (cnres).
        #
        cnres = Ngl.Resources()
        for t in dir(resources):
          if (t[0:2] == 'cn' or t[0:2] == 'sf' or t[0:3] == 'ngl'):
              setattr(cnres,t,getattr(resources,t))
        #
        cnres.cnLineLabelsOn    = False
        #
        if overlay_contour_lon != None:
            cnres.sfXArray        = overlay_contour_lon[:]
        else:
            cnres.sfXArray        = lon[:]                
        if overlay_contour_lon != None:
            cnres.sfYArray        = overlay_contour_lat[:]
        else:
            cnres.sfYArray        = lat[:]        
        #
        cnres.cnFillOn          = False
        cnres.cnLinesOn         = True
        cnres.nglDraw = False
        cnres.nglFrame = False
        cnres.lbLabelBarOn = False
        cnres.lbLabelsOn = False
        cnres.cnInfoLabelOn = False
        if overlay_contour_levels != None:
            cnres.cnLevelSelectionMode      = 'ExplicitLevels'
            cnres.cnLevels = overlay_contour_levels
        cnres.cnLineThicknessF  = 0.2
        if overlay_contour_colors != None:
            cnres.cnLineColors = overlay_contour_colors
        if overlay_contour_thickness != None:
            cnres.cnLineThicknessF  = overlay_contour_thickness
        #
        contour_overlay = Ngl.contour(wks, overlay_contour_data, cnres)
        Ngl.overlay(plot,contour_overlay)
        Ngl.draw(plot)

    IM = len(lon)
    JM = len(lat)

    for i in range(IM):
        for j in range(JM):
            if not delta_lon.mask[j,i]:
                # x = np.ma.masked_all(2)
                # y = np.ma.masked_all(2)
                # x[0],y[0] = lon[i],lat[j]
                # x[1],y[1] = lon[i] + delta_lon[j,i], lat[j] + delta_lat[j,i]
                x0, y0 = lon[i],lat[j]
                x1, y1 = lon[i] + delta_lon[j,i], lat[j] + delta_lat[j,i]
                if arrowsforwards:
                    x, y = make_arrow(x0, y0, x1, y1, arrowheadlength, arrowheadwidth, greatcircle=greatcircle)
                else:
                    x, y = make_arrow(x1, y1, x0, y0, arrowheadlength, arrowheadwidth, greatcircle=greatcircle)
                resources = Ngl.Resources()
                if vector_colors != None:
                    for k in range(len(vector_color_levels)):
                        if vector_colors[j,i] > vector_color_levels[k]:
                            marker_colorlevel[j,i] = marker_colorlevel[j,i]+1
                    resources.gsLineColor = colorbars_int[marker_colorlevel[j,i]]
                if vectorthickness != None:
                    resources.gsLineThicknessF  = vectorthickness
                pline = Ngl.polyline(wks,plot,x,y, resources)

    Ngl.draw(plot) 

    if not file==None:
        Ngl.delete_wks(wks)
        #
        if makepng:
            pdf_to_png(file, density=png_dens)
    else:
        x11_window_list.append(wks)






def make_arrow(x1, y1, x2, y2, arrowheadlength, arrowheadwidth, greatcircle=False):
    ### return a vector of points that define an arrow pointing from (x1, y1) to (x2, y2)

    mindist_greatcircle = 5.

    if greatcircle and ( Ngl.gc_dist(y1, x1, y2, x2) > mindist_greatcircle ) :
        npts_gc = int(Ngl.gc_dist(y1, x1, y2, x2))
        mean_x = (x1 + x2)/2.
        arrowbody_y,arrowbody_x = Ngl.gc_interp(y1, x1, y2, x2, npts_gc)
        dx = arrowbody_x[1:] - arrowbody_x[0:npts_gc-1]
        if np.absolute(dx).max() > 90.:
            # something funky with crossing the 0 or 180 debgree meridians
            arrowbody_y,arrowbody_x = Ngl.gc_interp(y1, x1, y2, x2, -npts_gc)
            # if np.all(arrowbody_x >= 0.):
            #     # 0-360 case
            #     arrowbody_x[arrowbody_x > 180.] = arrowbody_x[arrowbody_x > 180.] - 360.
            # else:
            #     # -180 to 180 case                
            #     arrowbody_x[arrowbody_x < 0.] = arrowbody_x[arrowbody_x > 180.] + 360.
            # print(dx)
            # print(arrowbody_x)
            # print(' ')
        lastsegment_x1 = arrowbody_x[npts_gc-2]
        lastsegment_x2 = arrowbody_x[npts_gc-1]
        lastsegment_y1 = arrowbody_y[npts_gc-2]
        lastsegment_y2 = arrowbody_y[npts_gc-1]
    else:
        lastsegment_x1 = x1
        lastsegment_x2 = x2
        lastsegment_y1 = y1
        lastsegment_y2 = y2


    if lastsegment_x1-lastsegment_x2 != 0. and lastsegment_y1-lastsegment_y2 != 0.:
        arrow_slope = (lastsegment_y2-lastsegment_y1)/(lastsegment_x2-lastsegment_x1)
        #
        transept_x = lastsegment_x2 - (lastsegment_y2-lastsegment_y1)/abs(lastsegment_y2-lastsegment_y1) * arrowheadlength * math.sin(math.atan(1./arrow_slope))
        transept_y = lastsegment_y2 - (lastsegment_y2-lastsegment_y1)/abs(lastsegment_y2-lastsegment_y1) * arrowheadlength * math.cos(math.atan(1./arrow_slope))
        #
        left_x = transept_x + 0.5 * arrowheadwidth * math.cos(math.atan(1./arrow_slope))
        left_y = transept_y - 0.5 * arrowheadwidth * math.sin(math.atan(1./arrow_slope))
        #
        right_x = transept_x - 0.5 * arrowheadwidth * math.cos(math.atan(1./arrow_slope))
        right_y = transept_y + 0.5 * arrowheadwidth * math.sin(math.atan(1./arrow_slope))

    else:
        # either horizontal or vertical
        if abs(lastsegment_x1-lastsegment_x2) < 1e-4:
            # vertical
            transept_x = lastsegment_x1
            transept_y = lastsegment_y2 - (lastsegment_y2-lastsegment_y1)/abs(lastsegment_y2-lastsegment_y1) * arrowheadlength
            left_x = transept_x + 0.5 * arrowheadwidth
            left_y = transept_y
            right_x = transept_x - 0.5 * arrowheadwidth
            right_y = transept_y
        if abs(lastsegment_y1-lastsegment_y2) < 1e-4:
            # horizontal
            transept_x = lastsegment_x2 - (lastsegment_x2-lastsegment_x1)/abs(lastsegment_x2-lastsegment_x1) *  arrowheadlength
            transept_y = lastsegment_y1
            left_x = transept_x
            left_y = transept_y + 0.5 * arrowheadwidth
            right_x = transept_x
            right_y = transept_y - 0.5 * arrowheadwidth
            


    if greatcircle and ( Ngl.gc_dist(y1, x1, y2, x2) > mindist_greatcircle ):
        x_vector = arrowbody_x.tolist()
        x_vector.extend([left_x, arrowbody_x[npts_gc-1], right_x])
        y_vector = arrowbody_y.tolist()
        y_vector.extend([left_y, arrowbody_y[npts_gc-1], right_y])
    else:
        x_vector = [x1, x2, left_x, x2, right_x]
        y_vector = [y1, y2, left_y, y2, right_y]

    return x_vector, y_vector


def make_logical_checkerboard(IM,JM):
    checkerboard = np.zeros([JM,IM], dtype=np.bool)
    for i in range(IM):
        for j in range(JM):
            checkerboard[j,i] = (j+i)%2 == 0
    return(checkerboard)


# def test_arrow():
#     length = 0.3
#     width = 0.1
#     x, y = make_arrow(0., 0., 1., 0.01,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 0.001, 1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., -1., 0.01,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 0.01, -1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., -1., -1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 1., 1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 0.3, 1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 1., 0.3,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., -1., 0.3,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., -1., -0.3,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., -1., 0.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 1., 0.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 0., 1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])
#     x, y = make_arrow(0., 0., 0., -1.,length, width)
#     xyplot(x, y, xrange=[-2,2], yrange=[-2,2])


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



def make_ellipse(x=0.0, y=0.0, a=0.0, b=0.0, angle=0.0, k=1./12):
    """ Draws an ellipse using (360*k + 1) discrete points; based on pseudo code
    given at http://en.wikipedia.org/wiki/Ellipse
    k = 1 means 361 points (degree by degree)
    a = major axis distance,
    b = minor axis distance,
    x = offset along the x-axis
    y = offset along the y-axis
    angle = clockwise rotation [in degrees] of the ellipse;
        * angle=0  : the ellipse is aligned with the positive x-axis
        * angle=30 : rotated 30 degrees clockwise from positive x-axis
    """
    pts_x = np.zeros((360*k+1))
    pts_y = np.zeros((360*k+1))    

    if angle == None:
        angle = 0.
    
    beta = -angle * np.pi/180.0
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    alpha = np.radians(np.r_[0.:360.:1j*(360*k+1)])
 
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    
    pts_x[:] = x + (a * cos_alpha * cos_beta - b * sin_alpha * sin_beta)
    pts_y[:] = y + (a * cos_alpha * sin_beta + b * sin_alpha * cos_beta)

    return pts_x, pts_y

def pairplot(data_array, colors=None, levels=None, title=None, file=None, datatitles=None, colormap=None, makepng=False, log_plots=None, position='ur', ranges=None, hist_sep=None, plot_hists=False, labelbar=False):
    """ This function creates a matrix of plots of data relative to each other, where diagonal elements are hsitograms and off-diagonal elements are xy plot.  
    Idea is similar to the pariplot routine in seaborne and pandas, but generalized to allow a last dimension that defines lines/curves rather than merely points in a space
    Possible values for position argument are 'ur' for upper right and 'll' for lower left"""
    #
    plot_type = get_workstation_type(file)
    #
    #
    possible_positions = ['ur','ll']
    if not position in possible_positions:
        raise Exception
    #
    wks_res = Ngl.Resources()
    if plot_type == 'x11':
        wks_res.wkPause = False
    elif plot_type == 'png':
        wks_res.wkWidth = page_width * 100
        wks_res.wkHeight = page_height * 100
    else:
        wks_res.wkPaperWidthF = page_width
        wks_res.wkPaperHeightF = page_height
        wks_res.wkOrientation = "portrait"
    #
    if not colormap == None:
        colormap = parse_colormap(colormap)
        wks_res.wkColorMap = colormap
    #    
    wks = Ngl.open_wks(plot_type,file,wks_res)
    if wks < 0 and plot_type == "x11":
        clear_oldest_x11_window()
        wks = Ngl.open_wks(plot_type,file,wks_res)
    #
    ndims_dataarray = len(data_array.shape)
    print(data_array.shape)
    n_dataframes = data_array.shape[-1]
    #
    plots = []
    #
    for ypos in range(n_dataframes):
        for xpos in range(n_dataframes):
            if ((ypos > xpos) and position == 'll') or ((ypos < xpos) and position == 'ur'):
                if ypos == n_dataframes-1 and position == 'll' and type(datatitles) != type(None):
                    xtitle=datatitles[xpos]
                elif ypos == xpos-1 and position == 'ur' and type(datatitles) != type(None):
                    xtitle=datatitles[xpos]
                else:
                    xtitle=' '
                #
                if xpos == 0 and position == 'll' and type(datatitles) != type(None):
                    ytitle=datatitles[ypos]
                elif xpos == ypos+1 and position == 'ur' and type(datatitles) != type(None):
                    ytitle=datatitles[ypos]
                else:
                    ytitle=' '
                #
                if type(log_plots) != type(None):
                    ylog = log_plots[ypos]
                    xlog = log_plots[xpos]
                else:
                    ylog = False
                    xlog = False
                #
                if ndims_dataarray == 3:
                    datax = data_array[:,:,xpos]
                    datay = data_array[:,:,ypos]
                else:
                    datax = data_array[:,xpos]
                    datay = data_array[:,ypos]                    
                #
                if type(ranges) == type(None):
                    rangex = [datax.min(), datax.max()]
                    rangey = [datay.min(), datay.max()]
                else:
                    rangex = ranges[xpos]
                    rangey = ranges[ypos]
                #
                plots.append(xyplot(datax, datay, linethickness=0.1, shaded_line_data=colors, shaded_line_levels=levels,xrange=rangex, yrange=rangey, use_wks=wks, ytitle=ytitle, xtitle=xtitle, xlog=xlog, ylog=ylog))
            elif xpos == ypos and plot_hists:
                #
                if ndims_dataarray == 3:
                    data_unsorted = data_array[:,:,xpos]
                else:
                    data_unsorted = data_array[:,xpos]                    
                print(data_unsorted.shape)
                print(hist_sep.shape)
                #
                if type(hist_sep) != type(None):
                    n_sorts = hist_sep.max()
                    nbins = data_unsorted.shape[0]
                    hist_sorted = data_unsorted.copy()
                    for i in range(nbins):
                        hist_sorted[i,0] = data_unsorted[i,hist_sep[i]]
                        hist_sorted[i,1] = data_unsorted[i,1-hist_sep[i]]                      
                if type(ranges) == type(None):
                    rangex = [data_unsorted.min(), data_unsorted.max()]
                else:
                    rangex = ranges[xpos]
                plots.append(plot_histogram(hist_sorted, use_wks=wks, therange=rangex, label_binedges=False, maxlabels=0))
            else:
                plots.append(0)
    #
    panel_res = Ngl.Resources()
    panel_res.nglPanelLabelBar = labelbar
    #
    Ngl.panel(wks, plots, [n_dataframes,n_dataframes], panel_res)
    #
    #Ngl.frame(wks)
    #
    if not file==None:
        Ngl.delete_wks(wks)
        #
        if makepng:
            pdf_to_png(file, density=png_dens)
    else:
        x11_window_list.append(wks)

        
def stemplot(data, parameter_labels=None, variable_labels=None, overlay_data=None, ranges=[0.,1.], file=None, makepng=False, png_dens=pngdens, use_wks=None, showjupyter=False, labels_space=0.1, margins_space=0.05, plot_xmargins=0.1, dotsize=0.02, parameter_labelsize=0.02, variable_labelsize=0.02, linethickness = 3., top_ticks=True, draw_boxes=True, width_factor = 1., maxticks=5, textthickness=1.5):
    """ this function makes one or more stemplots (i.e. look kind of like lollipops), as in for plotting parameter sensitivities.  
    plots are lined up vertically, with stes going to the right."""
    #
    plot_type = get_workstation_type(file)
    #
    #
    #
    wks_res = Ngl.Resources()
    #
    wks_res.nglMaximize = False
    wks_res.nglDraw     = False
    wks_res.nglFrame    = False
    #
    if plot_type == 'x11':
        wks_res.wkPause = False
    elif plot_type == 'png':
        wks_res.wkWidth = page_width * 100 * width_factor
        wks_res.wkHeight = page_height * 100
    else:
        wks_res.wkPaperWidthF = page_width * width_factor
        wks_res.wkPaperHeightF = page_height
        wks_res.wkOrientation = "portrait"
    #
    wks = Ngl.open_wks(plot_type,file,wks_res)
    if wks < 0 and plot_type == "x11":
        clear_oldest_x11_window()
        wks = Ngl.open_wks(plot_type,file,wks_res)
    #
    ## parse the shape of the data, and work from that.
    ndims_data = len(data)
    if ndims_data == 1:
        nvariables = 1
        nparameters = len(data)
    else:
        nvariables = data.shape[0]
        nparameters = data.shape[1]
    #
    if type(overlay_data) != type(None):
        if overlay_data.shape != data.shape:
            raise Exception
    #
    plots = []
    #
    if type(parameter_labels) != type(None):
        startindx = -1
        plots_startspace = labels_space + margins_space + plot_xmargins
    else:
        startindx = 0
        plots_startspace = plot_xmargins
    plots_width = (1. - (plots_startspace + plot_xmargins + margins_space * (nvariables-1))) / nvariables
    #
    datay = np.arange(nparameters)
    #
    for var_i in range(startindx,nvariables):
        if var_i < 0:
            ## this is for making the list of parameters
            plotres = Ngl.Resources()
            plotres.nglMaximize = False
            plotres.nglDraw     = False
            plotres.nglFrame    = False
            #
            # set size of viewport
            plotres.vpXF = plot_xmargins
            plotres.vpWidthF = labels_space
            #
            # set vertical boundaries of plot
            plotres.trYMinF = -nparameters
            plotres.trYMaxF = 1.
            plotres.trXMinF = -1.
            plotres.trXMaxF = 0.2
            plotres.tmXBOn          = False
            plotres.tmXTOn          = False
            plotres.tmYROn          = False
            plotres.tmYLOn          = False
            plotres.tmYRBorderOn    = False
            plotres.tmXBBorderOn    = False
            plotres.tmYLBorderOn    = False
            plotres.tmXTBorderOn    = False
            #
            plot = Ngl.blank_plot(wks, plotres)
            txres = Ngl.Resources()
            txres.txJust = "CenterRight"
            txres.txFontHeightF = parameter_labelsize
            txres.txFontThicknessF = textthickness
            for par_i in range(nparameters):
                txt = Ngl.add_text(wks, plot, parameter_labels[par_i], 0., -1.*par_i, txres)
        else:
            if ndims_data == 1:
                datax = data[:]
                if type(overlay_data) != type(None):
                    datax_overlay = overlay_data[:]
            else:
                datax = data[var_i,:]
                if type(overlay_data) != type(None):
                    datax_overlay = overlay_data[var_i,:]
            #
            xyplotres = Ngl.Resources()
            xyplotres.nglMaximize = False
            xyplotres.nglDraw     = False
            xyplotres.nglFrame    = False
            #
            # set size of viewport
            xyplotres.vpXF = plots_startspace + (var_i)*(margins_space + plots_width)
            xyplotres.vpWidthF = plots_width
            #
            # set  boundaries of plot
            xyplotres.trXMinF = ranges[0]
            xyplotres.trXMaxF = ranges[1]
            xyplotres.trYMinF = -nparameters
            xyplotres.trYMaxF = 1.
            #
            # title the plot
            xyplotres.tiMainString = variable_labels[var_i]
            xyplotres.tiMainFontHeightF = variable_labelsize
            xyplotres.tiMainFontThicknessF = textthickness
            if top_ticks:
                xyplotres.tmXBOn          = False
                xyplotres.tmXTOn          = True
                xyplotres.tmXUseBottom = False
                xyplotres.tmXTLabelsOn = True
                xyplotres.tmXTMinorOn    = False
                xyplotres.tmXTMaxTicks = maxticks
                xyplotres.tmXTLabelFontThicknessF = textthickness
            else:
                xyplotres.tmXBOn          = True
                xyplotres.tmXTOn          = False
                xyplotres.tmXBLabelsOn = True
                xyplotres.tmXBMinorOn    = False
                xyplotres.tmXBMaxTicks = maxticks
                xyplotres.tmXBLabelFontThicknessF = textthickness
            xyplotres.tmYROn          = False
            if draw_boxes:
                xyplotres.tmYRBorderOn    = True
                xyplotres.tmXBBorderOn    = True
            else:
                xyplotres.tmYRBorderOn    = False
                xyplotres.tmXBBorderOn    = False
            xyplotres.tmYROn                  = False
            xyplotres.tmYLOn                  = False
            #
            dummydata = np.ma.masked_all([2])
            plot = Ngl.xy(wks, dummydata, dummydata, xyplotres)
            #
            # now that we've set up plot, loop over variables and draw the content of the stemplot
            for par_i in range(nparameters):
                lineres = Ngl.Resources()
                lineres.gsLineThicknessF = linethickness
                Ngl.add_polyline(wks, plot, [0.,datax[par_i]], [-par_i,-par_i], lineres)
                #
                dotres = Ngl.Resources()
                dotres.gsMarkerIndex = 16
                dotres.gsMarkerSizeF = dotsize
                Ngl.add_polyline(wks, plot, [datax[par_i]], [-par_i], dotres)
                #
                if type(overlay_data) != type(None):
                    dotres = Ngl.Resources()
                    dotres.gsMarkerIndex = 4
                    dotres.gsMarkerSizeF = dotsize
                    Ngl.add_polyline(wks, plot, [datax_overlay[par_i]], [-par_i], dotres)
            #
        Ngl.draw(plot)
        del(plot)
    #
    #
    Ngl.frame(wks)
    #
    if not file==None:
        Ngl.delete_wks(wks)
        #
        if makepng or showjupyter:
            pdf_to_png(file, density=png_dens)
        if jupyter_avail and showjupyter:
            print(' ')
            display(Image(file+'.png'))
    else:
        x11_window_list.append(wks)
