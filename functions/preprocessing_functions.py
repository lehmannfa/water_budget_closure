import netCDF4
import numpy as np
import pandas as pd
import geopandas

def get_hydro_data(hydro_var_name,dataset,fill_value=-9999,path='../data/hydrology'):
    ''' format netCDF file to a table where each row is a grid point and each column is a month'''

    X=netCDF4.Dataset("{}/{}_{}.nc".format(path,hydro_var_name,dataset))

    # create time indices
    year=[d[3:] for d in np.asarray(X.variables['time'])]
    month=[d[:2] for d in np.asarray(X.variables['time'])]
    db=pd.DataFrame({'year':np.asarray(year).astype(int),
                    'month':np.asarray(month).astype(int),
                    'day':1})
    time_X=pd.to_datetime(db)

    # dataframe of all grid points
    lat=np.asarray(X.variables['Lat'])
    long=np.asarray(X.variables['Long'])
    (lat_flat,long_flat)=np.meshgrid(lat,long)
    df=pd.DataFrame({'x':long_flat.flatten(),'y':lat_flat.flatten()})
    spatial_grid=geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.x, df.y))

    # dataframe of each variable at each month over all grid point
    hydro_var=np.asarray(X.variables['{}_mm'.format(hydro_var_name)])

    # replace all missing values (=fill_value) by nans
    hydro_var=np.where(hydro_var==fill_value,np.nan,hydro_var)

    # hydro_var is of shape (nb_month x latitude points x longitude points
    Nx=hydro_var.shape[2]
    Ny=hydro_var.shape[1]
    Nt=time_X.shape[0]

    hydro_grid=hydro_var.T.reshape(Nx*Ny,Nt)
    hydro_grid=pd.DataFrame(hydro_grid,index=spatial_grid.index,columns=[d.date() for d in time_X])

    # join coordinates and hydrological variables
    return spatial_grid.join(hydro_grid),time_X