import numpy as np
import CreateGeoData as cgo
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geopandas


def plot_dataframe(proj, csv_file, ax, colum):
    """
    根据csv文件数据绘制地图
    :param proj:
    :param colum: 需要绘制的数据列名
    :param ax: 图片
    :param csv_file: geodataframe格式记录的数据
    :return:
    """
    df = cgo.read_geo_df(proj, csv_file)
    df = df.to_csv()
    df.plot(ax=ax, legend=True, column=df[colum], aspect=1, cmap='turbo')  # 绘制格子


def main(map_file, polygone_file, plot_data):
    proj = ccrs.LambertAzimuthalEqualArea(central_longitude=105, central_latitude=35, false_easting=6.0,
                                          false_northing=0.0, globe=None)  # 坐标系设定
    #proj = ccrs.EckertIII(central_longitude=30, false_easting=None, false_northing=None, globe=None)

    crs_proj4 = proj.proj4_init
    fig = plt.figure()  # 准备画图
    ax = fig.add_subplot(111, projection=proj)  # 增加子图
    ax.coastlines(resolution='50m', linewidth=0.5)
    #world_map = geopandas.read_file(map_file, crs='epsg:4326')  # read the map file
    #world_map = world_map.to_crs(crs_proj4)  # 转换地图坐标系
    #world_map.boundary.plot(ax=ax, linewidth=0.5)
    #world_map.plot(ax=ax, color='grey')  # 绘制地图
    gdf = cgo.read_geo_df('epsg:4326', polygone_file)  # 读取格子数据
    gdf = gdf.to_crs(crs_proj4)
    gdf.plot(ax=ax, legend=True, column=plot_data, aspect=1, cmap='OrRd', alpha=0.8)  # 绘制格子
    plt.xlim(-3000000, 3000000)
    plt.ylim(-2000000, 3000000)
    #ax.gridlines(
        #xlocs=np.arange(-180, 180 + 1, 10), ylocs=np.arange(-90, 90 + 1, 10),
        #draw_labels=True, x_inline=False, y_inline=False,
        #linewidth=0.5, linestyle='--', color='gray'
    #)  # 添加经纬度线
    plt.show()  # 显示图片


if __name__ == '__main__':
    main(map_file='../Map/World_Map_PC_YangYC/World_Map_PC_20181221.shp',
         polygone_file="../GridInfo/HD0711_match_1_.csv",
         plot_data="D_AV")
