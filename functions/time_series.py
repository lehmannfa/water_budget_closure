import numpy as np
import pandas as pd

def derivative(X,dt=1):
    ''' compute the 2 points derivative with centered difference'''
    Y=(1/(2*dt))*(X.values[2:]-X.values[:-2])
    return Y


def uncertainty_derivative(X):
    ''' convert uncertainties on TWS to uncertainties on TWSC'''
    Y=0.5*np.sqrt(X[2:].values**2+X[:-2].values**2)
    return Y


def time_filter(X):
    ''' filter to match derivation of TWS'''
    Y=0.25*X[:-2].values+0.5*X[1:-1].values+0.25*X[2:].values
    return Y


def area_square(lat,lat_res=0.5,long_res=0.5,a=6.378e6):
    ''' gives the area in km^2 of a square of length lat_res degree located at latitude lat'''
    radius=a*np.cos(lat*np.pi/180) # radius of the parallel supporting the square
    area=np.pi**2*a*radius/180**2 # area of a square of length 1°
    return area*lat_res*long_res/1e6


def weighted_average(hydro_basin,hydro_var_name,time_idx,lat_res=0.5,long_res=0.5,a=6.378e6):
    ''' compute the spatial average over a basin taking into account the Earth curvature
    if there are missing values, then the total area is slightly oversetimated compared to the area really covered by values'''
    area=area_square(hydro_basin['y'],lat_res=lat_res,long_res=long_res,a=a).values.reshape(hydro_basin.shape[0],1)
    total_area=np.sum(area)
    weighted_basin=hydro_basin[[d.date() for d in time_idx]]*area
    mean_basin=np.sum(weighted_basin,axis=0)/total_area # counts nans as zero
    return mean_basin


def get_hydro_timeseries(hydro_basin,hydro_var_name,time_idx,dataset_name,a=6.378e6,missing_threshold=5,lat_res=0.5,long_res=0.5,interpolation='cubic'):
    ''' if hydro_var_name is TWS, compute the 3 points derivative of TWS
    if hydro_var_name is not TWS, the function filters hydrological variables to match TWS derivation
    returns:
    - the weighted mean over the basin
    - the filtering of this weighted mean '''

    if hydro_var_name[:3]=='TWS': # we firstly need to interpolate the missing values from GRACE
        # interpolation can be performed only on dates
        df=pd.DataFrame(hydro_basin[[d.date() for d in time_idx]],columns=time_idx)
        df=df.interpolate(axis=1,method=interpolation)

        # replace missing values by the interpolated (others have not been changed)
        hydro_basin[[d.date() for d in time_idx]]=df

    elif np.isnan(hydro_basin[[d.date() for d in time_idx]]).sum().sum()>0: # perform a bilinear interpolation
        # interpolation can be performed only on dates
        df=pd.DataFrame(hydro_basin[[d.date() for d in time_idx]],columns=time_idx)
        df=df.interpolate(axis=1,method='linear')

        # replace missing values by the interpolated (others have not been changed)
        hydro_basin[[d.date() for d in time_idx]]=df

    # we check that the number of points with missing months does not exceed the threshold (in %)
    missing_points=hydro_basin.loc[np.sum(np.isnan(hydro_basin[[d.date() for d in time_idx]]),axis=1)>0].index
    if 100*missing_points.shape[0]/hydro_basin.shape[0]>missing_threshold:
        df=pd.Series(np.nan*np.ones(time_idx.shape[0]),index=time_idx)
        df_filter=pd.Series(np.nan*np.ones(time_idx.shape[0]-2),index=time_idx[1:-1])
        return df,df_filter

    # mean over the basin at each time point
    hydro_mean_basin=weighted_average(hydro_basin,hydro_var_name,time_idx,lat_res=lat_res,long_res=long_res,a=a)

    # if terrestrial water storage, we need to differentiate
    if hydro_var_name=='TWS':
        hydro_mean_basin_filter=derivative(hydro_mean_basin)

    # if water storage uncertainty, we apply the formula for uncertainty addition
    elif hydro_var_name=='TWS_uncertainty':
        hydro_mean_basin_filter=uncertainty_derivative(hydro_mean_basin)

    # otherwise, filtering to match the differential
    elif hydro_var_name in ['P','ET','R']:
        hydro_mean_basin_filter=time_filter(hydro_mean_basin)

    else:
        raise Exception('Variable {} is unknown'.format(hydro_var_name))

    # formatting
    df_filter=pd.Series(hydro_mean_basin_filter.flatten(),index=time_idx[1:-1],name='{} mean filtered'.format(hydro_var_name))
    return hydro_mean_basin,df_filter
