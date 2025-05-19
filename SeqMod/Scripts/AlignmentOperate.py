import random
import pandas
import SeqOperate


def read_fasta_as_df(file_fasta):
    """获得序列的字典 然后通过字典创建dataframe"""
    dic = SeqOperate.get_matrix_dic(file_fasta)
    return turn_fasta_as_df(dic)


def read_phy_as_df(file_phy):
    dic = SeqOperate.get_phy_dic(file_phy)
    return turn_fasta_as_df(dic)


def turn_fasta_as_df(dic):
    d = dic.copy()
    for key in d:
        d[key] = list(d[key])
    return pandas.DataFrame.from_dict(d)


def turn_df_as_fasta(df):
    """把df转换为fasta格式的字典"""
    dic = {}
    for label, content in df.items():
        bp_list = df[label].tolist()
        dic[label] = "".join(bp_list)
    return dic


def write_df_fasta(df, file):
    """把alignment以fasta格式写入文本文件"""
    dic = turn_df_as_fasta(df)
    with open(file, "w", encoding='utf-8') as matrix_file:
        for key in dic:
            matrix_file.write(f'>{key}\n{dic[key]}\n')


def write_df_phy(df, file):
    """把alignment以phy格式写入文本文件"""
    dic = turn_df_as_fasta(df)
    with open(file, "w", encoding='utf-8') as matrix_file:
        matrix_file.write(f' {len(dic)} {len(df)}\n')
        for key in dic:
            matrix_file.write(f'{key} {dic[key]}\n')


class Alignment:
    """Object of alignment
    把比对序列当作一个dataframe"""

    def __init__(self, df_align):
        self.pi = None
        self.hap_align = None
        self.hap = None
        self.alignment = df_align

    def snp_cites(self):
        """删除碱基完全一致的位点,只考虑ATCG"""
        print(self.alignment)
        need = []
        for index, row in self.alignment.iterrows():
            unique = list(set(row.tolist()))
            count = 0
            for ele in ["A", "T", "C", "G"]:
                if ele in unique:
                    count = count + 1
            if count > 1:
                need.append(index)
        print(need)
        self.alignment = self.alignment.iloc[need]

    def fill_with_most_fre(self):
        """使用位点最高频次的碱基填充序列中的缺失值"""
        df = self.alignment.copy()
        for index, row in df.iterrows():
            fre = row.value_counts()
            for i in fre.index:
                if i not in ["A", "T", "C", "G"]:
                    del fre[i]
            most_fre = fre.idxmax()
            row.replace('[^ATCG]', most_fre, inplace=True, regex=True)
        self.alignment = df

    def clean_missing_sites(self):
        """删除所有包含-的位点"""
        need = []
        for index, row in self.alignment.iterrows():
            row_ls = row.tolist()
            if "-" in row_ls:
                continue
            else:
                need.append(index)
        self.alignment = self.alignment.iloc[need]

    def random_sites(self, num):
        """随机挑选位点"""
        site_num = len(self.alignment)
        need = random.sample(range(1, site_num), num)
        self.alignment = self.alignment.iloc[need]

    def hap_generate(self):
        """生成单倍型序列文件，以及配套匹配表格"""
        df = self.alignment.copy()
        new_align = {}
        n = 0
        dic_hap_taxa = {}
        while len(df.columns.tolist()) > 1:
            n = n + 1
            hap_name = f'hap_{n}'
            print(hap_name)
            first_col = df.columns[0]
            print(first_col)
            taxa_ls = [first_col]
            seq = df[first_col].tolist()
            new_align[hap_name] = "".join(seq)  # 写入新的序列字典
            df = df.drop(first_col, axis=1)
            remove = []
            for column in df.columns.tolist():
                seq2 = df[column].tolist()
                if seq == seq2:  # 比较两个序列是否一致
                    remove.append(column)
                    taxa_ls.append(column)  # 一致就加入单倍型
            df = df.drop(remove, axis=1)  # 删除用过的序列
            dic_hap_taxa[hap_name] = taxa_ls
        self.hap = dic_hap_taxa  # 增加新的属性：单倍型-taxa列表
        self.hap_align = turn_fasta_as_df(new_align)  # 增加新的属性：单倍型-序列

    def filter_site(self, percent):
        """把比对序列修整齐,缺失率高于percent的删除"""
        # 计算每列中'-'的个数
        df = self.alignment.copy()
        # 计算每行中'-'的个数
        dash_count = df.apply(lambda row: (row == '-').sum(), axis=1)
        # 计算每行'-'值占总列数的比例
        dash_ratio = dash_count / df.shape[1]
        # 找出需要删除的行，比例大于等于x的行
        rows_to_drop = dash_ratio[dash_ratio >= percent].index
        # 删除这些行
        df_cleaned = df.drop(index=rows_to_drop)
        df_cleaned = df_cleaned.reset_index(drop=True)
        self.alignment = df_cleaned

    def pi_calculate(self):
        """计算序列的简约信息位点"""
        df = self.alignment.copy()
        valid_columns = 0
        # Loop through each column
        for col in df.columns:
            # Check if the column has at least two unique values
            if len(df[col].unique()) >= 2:
                # Check if each value in the column appears at least twice
                if df[col].value_counts().min() >= 2:
                    valid_columns += 1
        self.pi = valid_columns
