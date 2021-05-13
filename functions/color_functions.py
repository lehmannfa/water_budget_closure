from matplotlib.colors import Normalize #, ListedColormap, BoundaryNorm
#from matplotlib import cm
#import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np

# set the colormap and centre the colorbar
class MidpointNormalize(Normalize):
    """
    Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)

    e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    """
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))


def define_cmap(hydro_var_name,values):
    ''' called in each basin, for each hydrological variable, at a given month'''
    values=values[np.where(~np.isnan(values))]
    vmin=np.min(values)
    vmax=np.max(values)

    if hydro_var_name=='TWS':
        norm = MidpointNormalize(midpoint=0,vmin=vmin, vmax=vmax)
        cmap='RdBu'
    elif hydro_var_name=='P':
        norm = Normalize(vmin=0, vmax=vmax)
        cmap='Blues'
    elif hydro_var_name=='R':
        norm = Normalize(vmin=0, vmax=vmax)
        cmap='Purples'
    else: # ET
        norm = MidpointNormalize(midpoint=0,vmin=vmin, vmax=vmax)
        cmap='BrBG'
    return norm,cmap



# Each dataset is associated with a fixed color
colors_dataset={'ERA5_Land':'firebrick','MERRA2':'darkorange','JRA55':'tomato',
                'CPC':'olive','CRU':'forestgreen','GPCC':'limegreen',
                'GPCP':'mediumpurple','GPM':'rebeccapurple','TRMM':'hotpink',
                'MSWEP':'violet','GLDAS20':'lightpink',
                #'CLSM2.0':'teal','CLSM2.1':'lightgreen','CLSM2.2':'aquamarine',
                'GLDAS20_CLSM25':'teal','GLDAS21_CLSM25':'lightgreen','GLDAS22_CLSM25':'aquamarine',
                #'NOAH2.0':'lightskyblue','NOAH2.1':'deepskyblue',
                'GLDAS20_NOAH36':'lightskyblue','GLDAS21_NOAH36':'deepskyblue',
                #'VIC2.0':'blue','VIC2.1':'darkblue',
                'GLDAS20_VIC412':'blue','GLDAS21_VIC412':'darkblue',
                'GLEAM':'rebeccapurple','MOD16':'violet','SSEBop':'hotpink','FLUXCOM':'mediumpurple',
                'GRUN':'#eaee5e'
                }


climate_color_dict={'A': '#ff0000',
 'Af': '#960000',
 'Am': '#ff0000',
 'Afm':'#960000',
 'As': '#ff9999',
 'Aw': '#ffcccc',
 'Asw':'#ffcccc',
 'B': '#ccaa54',
 'BWk': '#ffff63',
 'BWh': '#ffcc00',
 'BSk': '#ccaa54',
 'BSh': '#cc8c14',
 'C': '#007800',
 'Cfa': '#003300',
 'Cfb': '#004f00',
 'Cfc': '#007800',
 'Cf': '#004f00',
 'Csa': '#00ff00',
 'Csb': '#95ff00',
 'Csc': '#c8ff00',
 'Cs': '#95ff00',
 'Cwa': '#593b00',
 'Cwb': '#966400',
 'Cwc': '#593b00',
 'D': '#ff6eff',
 'Dfa': '#330033',
 'Dfb': '#630063',
 'Dfc': '#c700c7',
 'Dfd': '#c71686',
 'Dsa': '#ff6eff',
 'Dsb': '#ffb5ff',
 'Dsc': '#e6c7ff',
 'Dsd': '#cccccc',
 'Dw': '#997fb3',
 'Dwa': '#c7b3c7',
 'Dwb': '#997fb3',
 'Dwc': '#8759b3',
 'Dwd': '#6d24b3',
 'E': '#6395ff',
 'EF': '#6395ff',
 'ET': '#63ffff'}





