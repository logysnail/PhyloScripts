import re
import CreateGeoData as cgd
import geopandas
import cartopy.crs as ccrs


def match_polygon(polygons, points, method):
    """

    :param polygons:
    :param points:
    :param method:
    :return:
    """
    polygons_with_info = polygons.copy()
    grid_num = len(polygons)
    for index_polygon, polygon in polygons.iterrows():  # 遍历格子
        index_points_matched = []
        grid_num = grid_num - 1
        print(f'Left: {grid_num} grid')  # 计数
        len_p = len(points)
        print(f'Points: {len_p}')
        if len_p == 0:  # 点是否匹配完了
            break
        else:
            for index_point, point in points.iterrows():  # 判断点是否在格子里
                if method == 'latlon':
                    judgement = point_in(str(point['geometry']), str(polygon['geometry']))
                    if judgement == 'in':
                        index_points_matched.append(point['pointID'])
                        points = points.drop(index=index_point)
                    if judgement == 'stop':
                        break  # 停止遍历节约时间。点按照经度排序。
                    else:
                        continue
                if method == 'shape':  # 不规则区域
                    go_poly = geopandas.GeoSeries(polygon['geometry'], crs="EPSG:4326")
                    go_point = geopandas.GeoSeries(data=point['geometry'], crs="EPSG:4326")
                    if go_poly.contains(go_point).bool():
                        index_points_matched.append(point['pointID'])
                        points = points.drop(index=index_point)
            polygons_with_info.loc[index_polygon, 'pointID'] = str(list(set(index_points_matched)))
            polygons_with_info.loc[index_polygon, 'num'] = str(len(index_points_matched))
    return polygons_with_info, points


def point_in(point, polygon):
    """
    判断一个点是否在经纬度格子里
    :param point: 点的数据
    :param polygon: 经纬度格子
    :return: 逻辑判断
    """
    if_in = ''
    point_match = re.search(r'\((.+)\)', point)
    if point_match:
        point = point_match.group(1)
        point_lon = float(point.split(" ")[0])
        point_lat = float(point.split(" ")[1])
        polygon_match = re.search(r'\(\((.+)\)\)', polygon)
        if polygon_match:
            polygon = polygon_match.group(1).split(", ")
            lons = []
            lats = []
            for top in polygon:
                lons.append(float(top.split(" ")[0]))
                lats.append(float(top.split(" ")[1]))
            polygon_lon_max = max(lons)
            polygon_lat_max = max(lats)
            polygon_lon_min = min(lons)
            polygon_lat_min = min(lats)
            if polygon_lon_max > point_lon > polygon_lon_min and polygon_lat_max > point_lat > polygon_lat_min:
                if_in = 'in'
            elif point_lon > polygon_lon_max:  # 点的经度大于格子最大经度，就返回停止匹配
                if_in = 'stop'
    return if_in


def main(polygone_df, point_file, method, polygone_csv, point_left):
    proj = ccrs.LambertAzimuthalEqualArea(central_longitude=90, central_latitude=0, false_easting=6.0,
                                          false_northing=0.0, globe=None)  # 坐标系设定
    crs_proj4 = proj.proj4_init

    grid_gdf = cgd.read_geo_df(crs_proj4, polygone_df)
    grid_gdf = cgd.read_geo_df('epsg:4326', polygone_df)
    point_gdf = cgd.format_points('epsg:4326', point_file)  # 读取点数据信息的源文件csv
    #point_gdf = point_gdf.to_crs(crs_proj4)
    print(point_gdf)

    r = match_polygon(grid_gdf, point_gdf, method)
    grid_gdf = r[0]
    points_left = r[1]
    grid_gdf.to_csv(polygone_csv)
    points_left.to_csv(point_left)


if __name__ == '__main__':
    main(polygone_df='../Grid/global_land_grid_complete_1.csv',
         point_file='../PointsOrigin/HD0711_xyj.csv',
         method='latlon',
         polygone_csv='../GridInfo/HD0711_match_1.csv',
         point_left='../PointsOrigin/HD0711_left.csv')
