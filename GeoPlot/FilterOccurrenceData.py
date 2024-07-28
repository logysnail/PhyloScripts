import os
import pandas


def colum_in_values(df, colum_list, values=None):
    """按照列值是否被包含筛选行，返回dataframe,支持多列"""
    if values is None:
        values = [True]
    for colum in colum_list:
        df = df[df[colum].isin(values)]
    return df


def range_values(df, colum, value1, value2):
    df = df[df[colum] <= value1 & df[colum] > value2]
    return df


def filter_distribution_data(file_path, out_path):
    occ = pandas.read_csv(file_path, delimiter="\t", index_col=0, on_bad_lines='warn')
    occ = colum_in_values(occ, ['hasCoordinate'])
    occ = colum_in_values(occ, ['taxonRank'], ['SPECIES'])
    #occ = occ[occ['coordinateUncertaintyInMeters'] <= 1000]
    occ = occ[['species', 'decimalLatitude', 'decimalLongitude']]
    occ.to_csv(out_path, sep="\t")


if __name__ == '__main__':
    original_occ_datas = "../GibifData/original/"
    for file in os.listdir(original_occ_datas):
        path = f'{original_occ_datas}{file}'
        path_out = f'../GibifData/Step1/{file.replace(".txt", ".csv")}'
        filter_distribution_data(path, path_out)
