import pandas


def adding_geo_data(point_csv, geo_csv):
    """
    根据点数据，以及匹配到格子里的点ID，在dataframe文件里添加想要绘制的数据列
    :return:新的geodataframe文件，添加了相关数据的新列
    """
    geo_df = pandas.read_csv(geo_csv, index_col=0)
    new_geo_df = geo_df.copy()
    point_df = pandas.read_csv(point_csv)
    for index_geo, row_geo in geo_df.iterrows():
        ids = eval(row_geo['pointID'])
        sp_list = []
        value = 0
        for num in ids:  # 遍历id
            v = point_df.loc[point_df['pointID'] == num]['d'].tolist()  # 按照index筛选并输出种名列表
            # sp_list = sp_list + sp_name  # 合并列表
            value = value + v[0]
        # sp_list = list(set(sp_list))
        if len(ids) > 0:
            value = value / len(ids)
        else:
            value = 0
        new_geo_df.loc[index_geo, 'D_AV'] = value
        # new_geo_df.loc[index_geo, 'hap_richness'] = len(sp_list)

    return new_geo_df


def main(point_csv, geo_csv, new_csv):
    new_geo_df = adding_geo_data(point_csv, geo_csv)
    new_geo_df.to_csv(new_csv)


if __name__ == '__main__':
    main('../PointsOrigin/HD0711_xyj.csv', '../GridInfo/HD0711_match_1.csv', '../GridInfo/HD0711_match_1_.csv')
