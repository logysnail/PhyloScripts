import re
import pandas


def read_hap_sample(file):
    """创建一个单倍型编号以及个体编号列表的对应字典"""
    dic = {}
    with open(file, "r") as hap_sample_file:
        lines = hap_sample_file.readlines()
        for line in lines:
            record = re.match('\[(.+):\s+\d+\s+([^]]+)]', line)
            hap = record.group(1)
            samples = record.group(2).split(" ")
            dic[hap] = samples
    return dic


def nex_format(file, csv_file):
    """根据state-sample-hap对应关系输出hap-states频次表"""
    df = pandas.read_csv(csv_file)
    dic = read_hap_sample(file)
    states = df['Distribution'].unique()
    df_hap_fre = pandas.DataFrame(0, columns=states, index=list(dic.keys()))
    for index in dic:
        samples = dic[index]
        state_list = []
        for sample in samples:
            distribution = df.loc[df[df.Sample == sample].index.tolist()[0], 'Distribution']
            state_list.append(distribution)
        print(state_list)
        for state in states:
            df_hap_fre.loc[index, state] = state_list.count(state)
    print(df_hap_fre)
    df_hap_fre.to_csv('E:/TG_ZCC/Network/PopNex_sp3.csv')


nex_format("E:/TG_ZCC/Network/GroupAlign/GroupAlign_sp3.nex", "E:/TG_ZCC/Network/DisIndi/DisIndi_sp3.csv")
