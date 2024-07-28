import geopandas
import pandas
import shapely
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from geodatasets import get_path
import numpy as np
from shapely.wkt import loads
import xarray as xr
import netCDF4 as nc

def create_lonlat_grid(degrees, lim):
    """
    沿着经纬度划分地图
    :param degrees : 每个格子是经纬度的几度
    :param lim: 格子覆盖的地球经纬度范围[lat1, lat2, lon1, lon2] 最大+-180/+-90
    :return: list_polygon 每个格子的四点坐标
    """
    lat1, lat2, lon1, lon2 = lim[0], lim[1], lim[2], lim[3]
    covered_degrees_lat = lat1
    covered_degrees_lon = lon1
    list_right = []
    list_down = []
    list_polygon = []
    while covered_degrees_lat < lat2:
        right = covered_degrees_lat + degrees
        list_right.append(right)
        covered_degrees_lat = right
    while covered_degrees_lon < lon2:
        down = covered_degrees_lon + degrees
        list_down.append(down)
        covered_degrees_lon = down
    for lat in list_right:
        for lon in list_down:
            left_up = [lon - degrees, lat]
            left_down = [lon - degrees, lat - degrees]
            right_up = [lon, lat]
            right_down = [lon, lat - degrees]
            list_polygon.append([right_up, right_down, left_down, left_up])
    return list_polygon


def create_square_grid(proj, gdf=None, bounds=None, n_cells=10, overlap=False):
    """Create square grid that covers a geodataframe area
    or a fixed boundary with x-y coords
    returns: a GeoDataFrame of grid polygons
    see https://james-brennan.github.io/posts/fast_gridding_geopandas/
    """
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
    else:
        xmin, ymin, xmax, ymax = gdf.total_bounds
    # get cell size
    cell_size = (xmax - xmin) / n_cells
    # create the cells in a loop
    grid_cells = []
    for x0 in np.arange(xmin, xmax + cell_size, cell_size):
        for y0 in np.arange(ymin, ymax + cell_size, cell_size):
            x1 = x0 - cell_size
            y1 = y0 + cell_size
            poly = shapely.geometry.box(x0, y0, x1, y1)
            # print (gdf.overlay(poly, how='intersection'))
            grid_cells.append(poly)
    cells = geopandas.GeoDataFrame(grid_cells, columns=['geometry'], crs=proj)
    if overlap:
        cols = ['grid_id', 'geometry', 'grid_area']
        cells = cells.sjoin(gdf, how='inner').drop_duplicates('geometry')
    return cells


def create_hex_grid(proj, gdf=None, bounds=None, n_cells=10, overlap=False):
    """Hexagonal grid over geometry.
    See https://sabrinadchan.github.io/data-blog/building-a-hexagonal-cartogram.html
    """
    if bounds is not None:
        xmin, ymin, xmax, ymax = bounds
    else:
        xmin, ymin, xmax, ymax = gdf.total_bounds

    unit = (xmax - xmin) / n_cells
    a = np.sin(np.pi / 3)
    cols = np.arange(np.floor(xmin), np.ceil(xmax), 3 * unit)
    rows = np.arange(np.floor(ymin) / a, np.ceil(ymax) / a, unit)
    hexagons = []
    for x in cols:
        for i, y in enumerate(rows):
            if i % 2 == 0:
                x0 = x
            else:
                x0 = x + 1.5 * unit

            hexagons.append(Polygon([
                (x0, y * a),
                (x0 + unit, y * a),
                (x0 + (1.5 * unit), (y + unit) * a),
                (x0 + unit, (y + (2 * unit)) * a),
                (x0, (y + (2 * unit)) * a),
                (x0 - (0.5 * unit), (y + unit) * a),
            ]))
    df = pandas.DataFrame(hexagons, columns=["polygon"])
    grid = geopandas.GeoDataFrame(df, crs=proj, geometry=df["polygon"])
    grid["grid_area"] = grid.area
    grid = grid.reset_index().rename(columns={"index": "grid_id"})
    if overlap:
        cols = ['grid_id', 'geometry', 'grid_area']
        grid = grid.sjoin(gdf, how='inner').drop_duplicates('geometry')
    return grid


def format_polygons(list_polygon):
    """
    获取多边形的GeoDataFrame
    :param list_polygon: 多边形顶点的列表的列表
    :return: GeoDataFrame对象
    """
    polygon_list = []
    for polygon_points_list in list_polygon:
        polygon_geom = Polygon(polygon_points_list)
        polygon_list.append(polygon_geom)
    df = pandas.DataFrame(polygon_list, columns=["polygon"])
    geo_dataframe = geopandas.GeoDataFrame(df, crs='epsg:4326', geometry=df["polygon"])
    return geo_dataframe


def format_points(proj, points_file):
    """
    根据点坐标文件输出GeoDataframe,根据经纬度排序
    经度升序，在此基础上纬度升序
    :param proj:
    :param points_file: 点的坐标csv文件
    :return: GeoDataframe
    """
    df = pandas.read_csv(points_file)
    df = df.sort_values(by=['Latitude'], ascending=[True])
    df = df.sort_values(by=['Longitude'], ascending=[True])
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude), crs=proj)
    print(gdf)
    return gdf


def read_geo_df(proj, gdf_csv):
    """
    geopandas生成的GeoDataframe文件在输出写入csv后不能直接读取为GeoDataframe对象
    所以需要这个步骤来读取为GeoDataframe对象
    :param proj: 读取的投影
    :param gdf_csv: geopandas生成的GeoDataframe 输出的 csv
    :return: GeoDataframe
    """
    grid_data = pandas.read_csv(gdf_csv, index_col=[0])  # 读取格子csv为Dataframe
    grid_data['geometry'] = grid_data['geometry'].apply(loads)  # 此步骤Dataframe才能被geopandas读取
    df = geopandas.GeoDataFrame(grid_data, crs=proj, geometry=grid_data['geometry'])  # 格子的GeoDataframe
    df = df.sort_values(by=['geometry'], ascending=[True])
    return df


def elevation_to_gdf(elevation_file):
    ds = nc.Dataset(elevation_file, 'r', format='NETCDF4')
    x = ds.variables['x'][:]
    y = ds.variables['y'][:]
    z = ds.variables['z'][:]
    data = []
    for index_lon in range(len(x)):
        for index_lat in range(len(y)):
            lon = x[index_lon]
            lat = y[index_lat]
            ele = z[index_lat][index_lon]
            data.append([lon, lat, ele])
    df = pandas.DataFrame(data, columns=["x", "y", "z"])
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.x, df.y), crs='epsg:4326')
    return gdf
