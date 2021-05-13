def decompose_combination(combination):
    iP=combination.find('_ET')
    data_P=combination[2:iP]
    iET=combination.find('_R')
    data_ET=combination[iP+4:iET]
    iR=combination.find('_TWS')
    data_R=combination[iET+3:iR]
    data_TWS=combination[iR+5:]

    return data_P,data_ET,data_R,data_TWS


def format_combination(comb):
    comb='P: '+comb[2:-22]
    comb=comb.replace('P: GLDAS20', 'P: PGF')
    comb=comb.replace('_ET_',' ; ET: ')
    comb=comb.replace('_R_',' ; R: ')

    comb=comb.replace('ERA5_Land','ERA5 Land')
    comb=comb.replace('GLDAS20_CLSM25','CLSM2.0')
    comb=comb.replace('GLDAS21_CLSM25','CLSM2.1')
    comb=comb.replace('GLDAS22_CLSM25','CLSM2.2')
    comb=comb.replace('GLDAS20_NOAH36','NOAH2.0')
    comb=comb.replace('GLDAS21_NOAH36','NOAH2.1')
    comb=comb.replace('GLDAS20_VIC412','VIC2.0')
    comb=comb.replace('GLDAS21_VIC412','VIC2.1')
    return comb


dict_dataset_name={'CLSM2.0':'GLDAS20_CLSM25','CLSM2.1':'GLDAS21_CLSM25','CLSM2.2':'GLDAS22_CLSM25',
                  'NOAH2.0':'GLDAS20_NOAH36','NOAH2.1':'GLDAS21_NOAH36','PGF':'GLDAS20',
                  'VIC2.0':'GLDAS20_VIC412','VIC2.1':'GLDAS21_VIC412',
                  'ERA5_Land':'ERA5 Land','MERRA2':'MERRA2','JRA55':'JRA55',
                   'CPC':'CPC','CRU':'CRU','GPCC':'GPCC','GPCP':'GPCP','GPM':'GPM',
                   'TRMM':'TRMM','MSWEP':'MSWEP','GLEAM':'GLEAM','MOD16':'MOD16',
                   'SSEBop':'SSEBop','FLUXCOM':'FLUXCOM','GRUN':'GRUN',
                   'GLDAS20_CLSM25':'CLSM2.0','GLDAS21_CLSM25':'CLSM2.1','GLDAS22_CLSM25':'CLSM2.2',
                   'GLDAS20_NOAH36':'NOAH2.0','GLDAS21_NOAH36':'NOAH2.1','GLDAS20':'PGF',
                   'GLDAS20_VIC412':'VIC2.0','GLDAS21_VIC412':'VIC2.1',
                   'ERA5 Land':'ERA5_Land',
                  }