import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle,ConnectionPatch

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


def popsicle_diagram(restartfile, param_file, pftcolors=['green','darkgreen'], stemcolor="brown", file=None, title=None, xtitle=None, ytitle=None, yrange=[0.,45.], colormap=None, title_charsize=0.75, aspect_ratio=None):


    # first calculate the crown areas of each cohort
    cohort_crownareas = carea_allom(restartfile, param_file)

    max_coh_per_patch = 100
    max_cohorts = len(restartfile.variables['fates_CohortsPerPatch'][:])
    max_patches = max_cohorts / max_coh_per_patch
    rects = []
    lines = []
    coordsA = "data"
    maxcanlev = restartfile.variables['fates_canopy_layer'][:].max()
    cohort_rhs = np.zeros(maxcanlev)
    ## iterate over patches
    patch_area_sofar = 0.
    #
    for i in range(max_patches):
        ## draw thin vertical line at patch lower boundary edge to delineate patches
        patch_lower_edge = 1.-patch_area_sofar - restartfile.variables['fates_area'][i*max_coh_per_patch]/1e4
        patchseparator = ConnectionPatch((patch_lower_edge,0),(patch_lower_edge,200),coordsA)
        #
        ## iterate over cohorts
        for l in range(maxcanlev-1,-1,-1):
            cohort_rhs = 1. - patch_area_sofar
            if restartfile.variables['fates_CohortsPerPatch'][i*max_coh_per_patch] > 0:
                for j in range(restartfile.variables['fates_CohortsPerPatch'][i*max_coh_per_patch]-1,-1,-1):
                    cindx = i * max_coh_per_patch + j
                    if restartfile.variables['fates_canopy_layer'][cindx]-1 == l:
                        rhs = cohort_rhs
                        lhs = rhs - cohort_crownareas[cindx]/1e4
                        ctop = restartfile.variables['fates_height'][cindx]
                        cbot = ctop * 0.6
                        crown = Rectangle((rhs, cbot), lhs-rhs, ctop-cbot, filled=True, ec='black', fc='green')
                        rects.append(crown)
                        #
                        stem_center = (lhs + rhs) /2.
                        stem_width = .00001 * restartfile.variables['fates_dbh'][cindx]
                        stem = Rectangle((stem_center-stem_width/2., 0.), stem_width, cbot, ec='black', fc=stemcolor)
                        rects.append(stem)
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
        # 
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for box in rects:
        ax.add_artist(box)
    ax.set_xlim(0, 1.)
    ax.set_ylim(yrange[0], yrange[1])
    #
    plt.show()
