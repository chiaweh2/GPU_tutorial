"""
rechunking the dataset into desired chunk

"""
import xarray as xr


def rechunk_spec(target_chunks, varname, compress=True, complevel=2):
    """
    The function create a encoding list for netcdf output
    the encoding_list need to be pass onto the encoding(kwarg)
    in .to_netcdf() method.

    Parameters
    ----------
    target_chunks : dictionary
        the python dictionary with include the coordinate name in 
        the same order as the dimension order in the variable.
        e.g. if the "q" has the dimension order of [t,z,y,x]
        the target_chunks = {
        't': t_chunksize,
        'z': z_chunksize,
        'y': y_chunksize,
        'x': x_chunksize,
        }

    varname : string
        the variable name in the Xarray dataset. 

    compress : boolean
        whether to perform compression or not. Default to True
        to perform compression
    
    complevel : integer 
        the compress level used when output to netCDF file.
        Value can range from 0-9 for zlib compression.
        Default compression level is set to 2
        for detail explanation please checkout
        https://www.unidata.ucar.edu/software/netcdf/workshops/most-recent/nc4chunking/CompressionAdvice.html

    Returns
    -------
    encoding_list : dict
        corresponding encoding for the DataArray in Dataset 
        to store in netCDF4 format.

    Raises
    ------

    """

    encoding_list = {}

    # variable encoding
    encoding_list[varname] = {}
    encoding_list[varname]['chunksizes'] = [*target_chunks.values()]
    encoding_list[varname]['contiguous'] = False
    encoding_list[varname]['zlib'] = compress
    encoding_list[varname]['complevel'] = complevel
    encoding_list[varname]['shuffle'] = True

    return encoding_list

if __name__ == '__main__':
    # Function rechunk_spec usage demo with Xarray
    ds = xr.open_dataset('/Projects/erai_modellevel/q_ml_1980_rechunked.nc')

    # one time one chunk file 
    #  make sure the order here is the exact right order
    #  of the data dimension order
    target_chunks = {
        'time': 1,
        'level': len(ds['level']),
        'latitude': len(ds['latitude']),
        'longitude': len(ds['longitude']),
        }

    encoding_list = rechunk_spec(target_chunks, varname='q', compress=True, complevel=2)

    # output netcdf file rechunked
    ds.to_netcdf('q_ml_1980.nc',encoding=encoding_list)
