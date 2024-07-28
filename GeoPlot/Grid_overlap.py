import CreateGeoData
import geopandas
import cartopy.crs as ccrs


def polygon_inside(polygon1, polygon2, grid_type):
    """
    将在polygon2内部的polygon1筛选并返回。
    :param grid_type: 多边形名称
    :param polygon1:需要筛选的多边形
    :param polygon2:作为条件的多边形
    :return:
    """
    new_polygon = geopandas.overlay(polygon2, polygon1, how='intersection', keep_geom_type=False).drop_duplicates(
        'geometry')
    print(new_polygon)
    new_polygon1 = new_polygon[
        new_polygon['polygon'].astype(str).str.len() == new_polygon['geometry'].astype(str).str.len()]
    new_polygon1.to_csv(f'../Grid/{grid_type}_complete_1.csv')
    new_polygon2 = new_polygon[
        new_polygon['polygon'].astype(str).str.len() != new_polygon['geometry'].astype(str).str.len()]
    new_polygon2.to_csv(f'../Grid/{grid_type}_incomplete_1.csv')


def main(grid_type, projection, map_gdf):
    if grid_type == 'latitude_longitude':
        new_grid = CreateGeoData.format_polygons(list_polygon=CreateGeoData.create_lonlat_grid(1, [-90, 90, -180, 180]))
        polygon_inside(new_grid, map_gdf, grid_type)
    if grid_type == 'hex_grid':
        map_gdf = map_gdf.to_crs(crs_proj4)
        bound = [-1000000, -1000000, 4000000, 4000000]
        new_grid = CreateGeoData.create_hex_grid(projection, gdf=map_gdf, bounds=bound, n_cells=200, overlap=False)
        new_polygon = geopandas.overlay(new_grid, map_gdf, how='intersection', keep_geom_type=False).drop_duplicates(
            'geometry')
        new_polygon.to_csv(f'../Grid/{grid_type}_200.csv')
    if grid_type == 'square_grid':
        new_grid = CreateGeoData.create_hex_grid(projection, gdf=map_gdf, bounds=None, n_cells=10, overlap=False)


if __name__ == '__main__':
    world_map = geopandas.read_file('../Map/ne_110m_land/ne_110m_land.shp')
    proj = ccrs.LambertAzimuthalEqualArea(central_longitude=90, central_latitude=0, false_easting=6.0,
                                          false_northing=0.0, globe=None)  # 坐标系设定
    crs_proj4 = proj.proj4_init
    main('hex_grid', crs_proj4, world_map)
