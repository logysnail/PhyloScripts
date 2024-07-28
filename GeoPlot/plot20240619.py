import numpy as np
import pandas
import CreateGeoData as cgo
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy
import LegendPlot as lp
import geopandas


def plot_dataframe():
    """
    根据csv文件数据绘制地图
    :param proj:
    :param colum: 需要绘制的数据列名
    :param ax: 图片
    :param csv_file: geodataframe格式记录的数据
    :return:
    """
    proj = ccrs.PlateCarree(central_longitude=150, globe=None)  # 坐标系设定
    #proj = ccrs.EckertIII(central_longitude=150, false_easting=None, false_northing=None, globe=None)
    crs_proj4 = proj.proj4_init
    df = change_grid_proj(crs_proj4)
    world_map = geopandas.read_file('../Map/ne_110m_land/ne_110m_land.shp')  # read the map file
    world_map = world_map.to_crs(crs_proj4)  # 转换地图坐标系
    df = merge_data(df, "E:/GenusRichness_PP/grid_ACseedgen_allGR_sharedSR.csv")  # 拼合格子以及格子数据
    # df = cgo.read_geo_df('epsg:4326', csv_file)  # 读取 格子文件 2度 带数据
    # df = df.to_crs(crs_proj4)  # 转换格子坐标系
    genus_list = pandas.read_csv("E:/GenusRichness_PP/ACshared_seedgen_SR&shSR_count_c.csv")  # 读取所有属名的列表
    for index, row in genus_list.iterrows():  # 遍历属名作图
        genus_code = row['gencode']
        sr = genus_code + "_SR"
        shSR = genus_code + "_shSR"
        title = f'${row["gen"]}$ ({row["ord"]}, {row["fam"]})'
        single_plot(sr, shSR, df, proj, title, genus_code)


def merge_data(grid_gdf, csv_data):
    """
    合并数据
    """
    df_data = pandas.read_csv(csv_data, index_col="Id")
    df = grid_gdf.join(df_data)
    df.replace(0.0, np.nan)
    df.to_csv("../GridInfo/species_2degree_pp.csv")
    return df


def set_color_map():
    cdict1 = {'red': [(0.0, 1.0, 1.0),
                      (1.0, 1.0, 1.0)],
              'green': [(0.0, 1.0, 1.0),
                        (1.0, 0.0, 0.0)],
              'blue': [(0.0, 1.0, 1.0),
                       (1.0, 0.2, 0.2)]}

    cdict2 = {'red': [(0.0, 1.0, 1.0),
                      (1.0, 0.0, 0.0)],
              'green': [(0.0, 1.0, 1.0),
                        (1.0, 0.27, 0.27)],
              'blue': [(0.0, 1.0, 1.0),
                       (1.0, 1.0, 1.0)]}
    cmapx = mpl.colors.LinearSegmentedColormap('cc', cdict1)
    cmapy = mpl.colors.LinearSegmentedColormap('cc', cdict2)
    cmapx.set_under('grey')
    cmapy.set_under('grey')
    return cmapx, cmapy


def single_plot(plot_column_1, plot_column_2, df, proj, title, file_name):
    """
    循环绘制单个地图输出为jpg格式
    :param file_name:
    :param title: 图片标题
    :param plot_column_1: x轴数据列名
    :param plot_column_2: y轴数据列名
    :param df: GeoDataframe
    :param proj: 投影
    :return:
    """
    fig = plt.figure(figsize=(12, 5), facecolor="grey")  # 准备画图
    ax = fig.add_subplot(111, projection=proj)  # 增加子图
    ax.set_position(pos=[0, 0, 1, 1])  # 使得子图填充整个图片 位置0，0 比例1，1
    cmap_x, cmap_y = set_color_map()  # 设置颜色color map
    ax.coastlines(resolution='110m', linewidth=0.2)  # 设置颜色color map
    df.plot(ax=ax, legend=False, column=plot_column_1, cmap=cmap_x, alpha=0.8, linewidth=1)  # 数据1
    df.plot(ax=ax, legend=False, column=plot_column_2, cmap=cmap_y, alpha=0.5, linewidth=1)  # 数据2
    plt.ylim(-60, 90)  # 除去南纬60以上部分
    ax.spines['top'].set_linewidth(0.1)
    ax.spines['bottom'].set_linewidth(0.1)
    ax.spines['left'].set_linewidth(0.1)
    ax.spines['right'].set_linewidth(0.1)  # 设置框线
    #plt.text(0, 81, title, horizontalalignment='center', fontsize=20)  # 设置题图

    ax2 = fig.add_axes([0.03, 0.05, 1 / 10.5, 1 / 5])  # add new axes to place the legend there and specify its location
    range_x = df[plot_column_1].max()
    range_y = df[plot_column_2].max()  # 数据范围
    #range_y = 1
    lp.two_factor_legend_continue(ax2, range_x, range_y, cmap_x, cmap_y)  # 绘制二因素图例
    plt.savefig(f"E:/GenusRichness_PP/{file_name}.jpg", dpi=600)
    plt.close()


def change_grid_proj(proj):
    geo_df = geopandas.read_file('E:/py/GeoTools/Map/global_grid_hhh/global_grid.shp')  # read the map file
    geo_df = geo_df.to_crs(proj)
    print(geo_df)
    geo_df.to_csv('E:/py/GeoTools/Map/hhh_grid')
    return geo_df


def main():
    plot_dataframe()


if __name__ == '__main__':
    main()
