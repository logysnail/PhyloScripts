import os

import pandas

import FileOperate
import SeqOperate


def search_database(database_folder, acc):
    """
    在指定文件夹中搜索包含特定 accession number (acc) 的 CSV 文件，并生成一个新名称。

    参数：
    - database_folder: str, 数据库文件夹路径，里面包含多个 CSV 文件
    - acc: str, 要搜索的 accession number（比如基因或序列的标识符）

    返回：
    - new_name: str, 格式为 'fam%sp_name%acc' 的新名称，如果没找到则返回 None
    """

    # 遍历数据库文件夹中的所有文件
    for file_name in os.listdir(database_folder):
        # 从文件名中移除 '.csv' 后缀，得到家族名 (fam)
        fam = file_name.replace(".csv", "")

        # 读取当前 CSV 文件为 DataFrame，使用 UTF-8 编码
        df = pandas.read_csv(f'{database_folder}/{file_name}', encoding='utf-8')

        # 检查 DataFrame 中每行是否有列包含 acc（仅对字符串类型检查）
        # applymap: 对每个单元格应用 lambda 函数，检查是否为字符串且包含 acc
        # any(axis=1): 按行检查是否有任意列满足条件
        # index: 获取满足条件的行索引
        indices = df[df.applymap(lambda x: isinstance(x, str) and acc in x).any(axis=1)].index

        # 如果没有找到匹配的行（indices 为空），跳过当前文件
        if indices.empty:
            continue

        # 如果找到匹配行，从 'sp' 列中提取物种名 (sp_name)，并移除索引显示
        else:
            sp_name = df.loc[indices, 'sp'].to_string(index=False)

            # 构建新名称：fam%sp_name%acc
            # sp_name 中的空格替换为下划线
            new_name = f'{fam}%{sp_name.replace(" ", "_")}%{acc}'

            # 找到匹配后直接返回新名称，结束函数
            return new_name
    # 如果遍历完所有文件都没找到，返回 None（隐式）


def name_changes(fasta_file, database_folder, out_folder):
    print(fasta_file)
    seq_dic = SeqOperate.get_matrix_dic(fasta_file)
    new_dic = {}
    for seq_name in seq_dic:
        try:
            new_name = search_database(database_folder, seq_name)
            new_dic[new_name] = seq_dic[seq_name].replace(".", "")
        except:
            print(seq_name)
            continue
    SeqOperate.rmix(f'{out_folder}/{os.path.basename(fasta_file)}', new_dic)


def fam_marker_rename(fasta_folders, changed_folders, database_folder):
    for folder in os.listdir(fasta_folders):
        out_folder = f'{changed_folders}/{folder}'
        fasta_folder = f'{fasta_folders}/{folder}'
        print(fasta_folder)
        FileOperate.makedir(out_folder)
        FileOperate.loop_folder_1(name_changes, fasta_folder, database_folder=database_folder, out_folder=out_folder)


def main():
    database_folder = "E:/Global_mega_diversification/SequenceData/NCBIData/GBs_matrix"
    fasta_folders = "E:/Global_mega_diversification/SequenceData/NCBIData/全cp提取cp数据"
    changed_folders = "E:/Global_mega_diversification/SequenceData/NCBIData/全cp提取cp数据_mod"
    FileOperate.makedir(changed_folders)
    fam_marker_rename(fasta_folders, changed_folders, database_folder)


if __name__ == "__main__":
    main()
