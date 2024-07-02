import pandas
import SeqOperate


def read_fasta_as_df(file_fasta):
    dic = SeqOperate.get_matrix_dic(file_fasta)
    return pandas.DataFrame.from_dict(dic)


def turn_df_as_fasta(df):
    """把df转换为fasta格式的字典"""
    dic = {}
    for label, content in df.items():
        bp_list = df[label].tolist()
        dic[label] = "".join(bp_list)
    return dic


class Alignment:
    """Object of alignment
    把比对序列当作一个dataframe"""

    def __init__(self, df_align):
        self.alignment = df_align

    def snp_cites(self):
        """删除碱基完全一致的位点,只考虑ATCG"""
        need = []
        for index, row in self.alignment.iterrows():
            unique = list(set(row.tolist()))
            count = 0
            for ele in ["A", "T", "C", "G"]:
                if ele in unique:
                    count = count + 1
            if count > 1:
                need.append(index)
        self.alignment = self.alignment.iloc[need]

    def fill_missing_with_most_fre(self):
        """使用位点最高频次的碱基填充序列中的缺失值"""
        for index, row in self.alignment.iterrows():
            fre = row.value_counts()
            if "-" in fre:
                del fre["-"]
            most_fre = fre.idxmax()
            row.replace('[^ATCG]', most_fre, inplace=True, regex=True)

    def write_align_fasta(self, file):
        """把alignment以fasta格式写入文本文件"""
        dic = turn_df_as_fasta(self.alignment)
        with open(file, "w", encoding='utf-8') as matrix_file:
            for key in dic:
                matrix_file.write(f'>{key}\n{dic[key]}\n')
