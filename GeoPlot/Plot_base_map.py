import re
import numpy
import numpy as np
import pandas
import netCDF4 as nc
import CreateGeoData as cgo
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geopandas
import GeoPlots
import xarray as xr
import matplotlib as mpl


def plot_contourf(elevation_csv, ax, proj):
    ele = nc.Dataset('../Map/ETOPO2v2c_f4.nc', 'r')
    # 获取经度和纬度变量
    print(ele)
    lon_var = ele.variables['x'][:]
    lat_var = ele.variables['y'][:]
    ele_var = ele.variables['z'][:]
    ele.close()
    cmap = (mpl.colors.ListedColormap(['#bbd2c5', '#536976', '#292e49'])
            .with_extremes(over='#292e49', under='#F0FFFF'))
    # ax.contourf(lon_var, lat_var, ele_var, transform=proj)
    ax.pcolor(lon_var, lat_var, np.squeeze(ele_var))
    plot_contourf('../Map/ETOPO2v2c_f4.nc', ax, proj)  # 绘制等高线


def main(map_file, polygone_file, plot_data):
    proj = ccrs.LambertAzimuthalEqualArea(central_longitude=90, central_latitude=0, false_easting=6.0,
                                          false_northing=0.0, globe=None)  # 坐标系设定
    fig, ax = plt.subplots(subplot_kw={'projection': proj}, figsize=(10, 5))
    plot_contourf(elevation_csv, ax, proj)


if __name__ == '__main__':
    main(map_file='../Map/ne_110m_land/ne_110m_land.shp',
         polygone_file="../GridInfo/TG_match_Hap_hex.csv",
         plot_data="hap_richness")
