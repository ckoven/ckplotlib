import numpy as np
import Ngl
import sys
from map_funcs import get_workstation_type,parse_colormap,clear_oldest_x11_window,x11_window_list,pngdens,page_width,page_height,jupyter_avail


def carea_allom(rest_fin, paramfin):
    ncohorts_max = len(rest_fin.variables['fates_CohortsPerPatch'][:])
    pft = rest_fin.variables['fates_pft'][:]
    dbh = rest_fin.variables['fates_dbh'][:]
    carea = np.ma.masked_all(ncohorts_max)
    fates_allom_cmode = paramfin.variables['fates_allom_cmode'][:]
    if np.any(fates_allom_cmode != 1):
        raise Exception
    carea_exp = paramfin.variables['fates_allom_d2bl2'][:]
    fates_allom_d2ca_coefficient_max = paramfin.variables['fates_allom_d2ca_coefficient_max'][:]
    fates_allom_d2ca_coefficient_min = paramfin.variables['fates_allom_d2ca_coefficient_min'][:]
    fates_allom_blca_expnt_diff = paramfin.variables['fates_allom_blca_expnt_diff'][:]
    fates_spread = rest_fin.variables['fates_spread'][:]
    fates_nplant = rest_fin.variables['fates_nplant'][:]
    fates_allom_dbh_maxheight = paramfin.variables['fates_allom_dbh_maxheight'][:]
    d2ca_coeff = fates_allom_d2ca_coefficient_max * fates_spread + fates_allom_d2ca_coefficient_min * (1.-fates_spread)
    for i in range(ncohorts_max):
        if pft[i] > 0:
            eff_dbh = np.min([dbh[i], fates_allom_dbh_maxheight[pft[i]-1]])
            print(eff_dbh)
            carea[i] = d2ca_coeff[pft[i]-1] * (eff_dbh ** (carea_exp[pft[i]-1] + fates_allom_blca_expnt_diff[pft[i]-1])) * fates_nplant[i]
    return carea


def popsicle_diagram(restartfile, param_file, pftcolors, stemcolor=159, file=None, title=None, xtitle=None, ytitle=None, yrange=None, colormap=None, title_charsize=0.75, aspect_ratio=None, makepng=False, png_dens=pngdens, use_wks=None, showjupyter=False):

    if use_wks == None:
        plot_type = get_workstation_type(file)
        
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

    if yrange != None:
        resources.trYMinF = np.min(yrange)
        resources.trYMaxF = np.max(yrange)

    resources.trXMinF = 0.
    resources.trXMaxF = 1.

    resources.tiMainFontHeightF = 0.025 * title_charsize

    resources.tmXBMajorLengthF        = 0.01
    resources.tmXBMajorOutwardLengthF = 0.01
    resources.tmYLMajorLengthF        = 0.01    
    resources.tmYLMajorOutwardLengthF = 0.01

    resources.tmXBMinorOn    = False
    resources.tmYLMinorOn    = False

    resources.tmXTOn          = False
    resources.tmYROn          = False
    resources.tmXBOn          = False
    resources.tmXBLabelsOn    = False

    if aspect_ratio != None:
        if aspect_ratio > 1.:
            resources.vpHeightF =  0.6  / aspect_ratio
        else:
            resources.vpWidthF =  0.6  * aspect_ratio

    resources.trXMinF = 0.
    resources.trXMaxF = 1.
    if yrange == None:
        yrange = [0, np.ma.max(restartfile.variables['fates_height'][:])]
    resources.trYMinF = np.min(yrange)
    resources.trYMaxF = np.max(yrange)

    dummies = np.ma.masked_all(3)
    plot = Ngl.xy(wks, dummies, dummies, resources)

    #### the main logic all goes here.  ####

    # first calculate the crown areas of each cohort
    cohort_crownareas = carea_allom(restartfile, param_file)

    max_coh_per_patch = 100
    max_cohorts = len(restartfile.variables['fates_CohortsPerPatch'][:])
    max_patches = max_cohorts / max_coh_per_patch
    maxcanlev = restartfile.variables['fates_canopy_layer'][:].max()
    cohort_rhs = np.zeros(maxcanlev)
    ## iterate over patches
    patch_area_sofar = 0.
    vline_res = Ngl.Resources
    vline_res.gsLineThicknessF = .01
    #
    crown_res = Ngl.Resources()
    crown_res.gsLineColor            = "black"
    crown_res.gsLineThicknessF       = .01
    crown_res.gsEdgesOn              = True
    crown_res.gsFillOpacityF         = 0.5
    #
    shadow_res = Ngl.Resources()
    shadow_res.gsFillColor            = "black"
    shadow_res.gsEdgesOn              = False
    #
    stem_res1 = Ngl.Resources()
    stem_res1.gsLineThicknessF       = 1.
    stem_res1.gsEdgesOn              = True
    stem_res1.gsLineColor            = "black"
    #
    stem_res2 = Ngl.Resources()
    stem_res2.gsEdgesOn              = False
    stem_res2.gsFillOpacityF         = 1.
    #
    for i in range(max_patches):
        ## draw thin vertical line at patch lower boundary edge to delineate patches
        patch_lower_edge = 1.-patch_area_sofar - restartfile.variables['fates_area'][i*max_coh_per_patch]/1e4
        zlx = [patch_lower_edge, patch_lower_edge]
        zly = [0., 1000.]
        Ngl.add_polyline(wks,plot, zlx, zly, vline_res)
        #
        ## iterate over cohorts
        for l in range(maxcanlev-1,-1,-1):
            shadow_res.gsFillOpacity = l * 0.5
            cohort_rhs = 1. - patch_area_sofar
            if restartfile.variables['fates_CohortsPerPatch'][i*max_coh_per_patch] > 0:
                for j in range(restartfile.variables['fates_CohortsPerPatch'][i*max_coh_per_patch]-1,-1,-1):
                    cindx = i * max_coh_per_patch + j
                    if restartfile.variables['fates_canopy_layer'][cindx]-1 == l:
                        rhs = cohort_rhs
                        lhs = rhs - cohort_crownareas[cindx]/1e4
                        ctop = restartfile.variables['fates_height'][cindx]
                        cbot = ctop * 0.6
                        crown_res.gsFillColor = pftcolors[restartfile.variables['fates_pft'][cindx]-1]
                        px = [rhs,rhs,lhs,lhs,rhs]
                        py = [ctop,cbot,cbot,ctop,ctop]
                        #
                        stem_center = (lhs + rhs) /2.
                        stem_width = .00001 * restartfile.variables['fates_dbh'][cindx]
                        stem_res2.gsFillColor = stemcolor
                        sx = [stem_center+stem_width,stem_center+stem_width,stem_center-stem_width,stem_center-stem_width,stem_center+stem_width]
                        sy = [cbot,0.,0.,cbot,cbot]
                        Ngl.add_polyline(wks,plot,sx,sy,stem_res1)
                        Ngl.add_polygon(wks,plot,sx,sy,stem_res2)
                        #
                        if l > 0:
                            Ngl.add_polygon(wks,plot,px,py,shadow_res)
                        #
                        Ngl.add_polygon(wks,plot,px,py,crown_res)
                        #
                        cohort_rhs = lhs
                        #if lhs < patch_lower_edge:
                        #    raise Exception
        #
        ## get cohort properties: height, upper horizontal edge, crown area, pft, canopy layer
        #
        ## draw cohort as popsicle
        #
        patch_area_sofar = patch_area_sofar + restartfile.variables['fates_area'][i*max_coh_per_patch]/1e4
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
                print('showing file '+file)
                display(Image(file+'.png'))
        else:
            x11_window_list.append(wks)
    else:
        return plot

