import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import xarray as xr
import random
import csv


def set_map_extent_and_ticks(
        ax, extents, proj, x_ticks, y_ticks, nx=0, ny=0,
        x_formatter=None, y_formatter=None):
    """
    :param ax: 目标地图.支持_RectangularProjection和Mercator投影.
    :param extents:经纬度范围[lonmin, lonmax, latmin, latmax].值为None表示全球.
    :param x_ticks:经度主刻度的坐标.
    :param y_ticks:纬度主刻度的坐标.
    :param proj:投影方式
    :param nx:经度主刻度之间次刻度的个数.默认没有次刻度.
            当经度不是等距分布时,请不要进行设置.
    :param ny:int, optional
            纬度主刻度之间次刻度的个数.默认没有次刻度.
            当纬度不是等距分布时,请不要进行设置.
    :param x_formatter:Formatter, optional
            经度主刻度的Formatter.默认使用无参数的LongitudeFormatter.
    :param y_formatter:Formatter, optional
            纬度主刻度的Formatter.默认使用无参数的LatitudeFormatter.
    :return:没有
    """
    # 设置主刻度.
    ax.set_xticks(x_ticks, crs=proj)
    ax.set_yticks(y_ticks, crs=proj)
    # 设置次刻度.
    xlocator = mticker.AutoMinorLocator(nx + 1)
    ylocator = mticker.AutoMinorLocator(ny + 1)
    ax.xaxis.set_minor_locator(xlocator)
    ax.yaxis.set_minor_locator(ylocator)
    # 设置Formatter.
    if x_formatter is None:
        x_formatter = LongitudeFormatter()
    if y_formatter is None:
        y_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(x_formatter)
    ax.yaxis.set_major_formatter(y_formatter)
    if extents is None:
        ax.set_global()
    else:
        ax.set_extent(extents, crs=proj)


def add_shapefile(ax, proj, shape_file, **feature_kw):
    """
    在地图上画出中国省界的shapefile.

    Parameters
    ----------
    **feature_kw
        调用add_feature时的关键字参数.
        例如linewidth,edgecolor和facecolor等.
    :param shape_file:
    :param ax: GeoAxes
        目标地图.
    :param proj: 投影方式
    """
    reader = shpreader.Reader(shape_file)
    geometries = reader.geometries()
    provinces = cfeature.ShapelyFeature(geometries, proj)
    ax.add_feature(provinces, **feature_kw)


def add_box_on_map(ax, extents, proj, **rect_kw):
    """
    在地图上画出一个方框.
    Parameters
    ----------
    **rect_kw
        创建Rectangle时的关键字参数.
        例如linewidth, edgecolor和facecolor等.
    :param ax: GeoAxes
        目标地图.最好为矩形投影,否则效果可能很糟.
    :param extents: 4-tuple of float
        方框的经纬度范围[lonmin, lonmax, latmin, latmax].
    :param proj: projection
    """
    lonmin, lonmax, latmin, latmax = extents
    rect = mpatches.Rectangle(
        (lonmin, latmin), lonmax - lonmin, latmax - latmin,
        transform=proj, **rect_kw
    )
    ax.add_patch(rect)


def read_loc(filename):
    """
    :param filename: 文件路径 文件每行 key,lat,lon
    :return: 返回同名点的经纬度列表字典
    """
    dic_key_loc = {}
    with open(filename, "r") as loc_file:
        loc_info = csv.reader(loc_file)
        next(loc_info)
        for row in loc_info:
            print(row)
            lat = row[1]
            lon = row[2]
            key = row[0]
            loc = [lat, lon]
            if key in dic_key_loc:
                dic_key_loc[key].append(loc)
            if key not in dic_key_loc:
                ls = [loc]
                dic_key_loc[key] = ls
    return dic_key_loc


def plot_dots(ax, dic, key, shape, **plot):
    """
    :param ax: 目标图
    :param dic: 储存点经纬度的字典 类别：[[]]
    :param key: 需要画的点的类别
    :param shape: 点的形状
    **plot：其他plot参数
    :return:
    """
    for era in dic:
        if era == key:
            ls = dic[era]
            lats = []
            lons = []
            for loc in ls:
                lats.append(float(loc[0]))
                lons.append(float(loc[1]))
            ax.plot(lons, lats, shape, label=era, **plot)


def random_color():
    return "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])





