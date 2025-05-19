import SeqOperate
import os
from collections import defaultdict

"""
合并文件夹内数个二级文件夹的同名文件"""


def merge_gene_files(input_folder, output_folder):
    # 获取文件夹中所有文件
    files = [f for f in os.listdir(input_folder) if f.endswith('.fasta')]
    # 用一个字典来存储按照 'gene数字' 分组的文件内容
    gene_dict = defaultdict(list)
    # 遍历所有文件，根据 'gene数字' 分组
    for file in files:
        # 提取文件名中的 'gene数字'
        gene_number = file.split('_')[1].replace('re', '')
        # gene_number = file.replace('', '')
        # 构建完整的文件路径
        file_path = os.path.join(input_folder, file)
        # 读取文件内容并添加到对应的 gene_number 分组中
        with open(file_path, 'r') as f:
            gene_dict[gene_number].append(f.read())
    # 对每个 gene_number，创建一个文件并将合并后的文件写入其中
    for gene_number, contents in gene_dict.items():
        # 创建文件，名称为 'gene数字'
        output_file_path = os.path.join(output_folder, f'001_{gene_number}')
        print(output_file_path)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # 合并内容
        merged_content = "".join(contents)
        with open(output_file_path, 'w') as output_file:
            output_file.write(merged_content)


def main():
    path_root = "E:/Global_mega_diversification/Data_Vitaceae/Nuc229_Vitaceae"
    merge_gene_files(f'{path_root}/250219_all',
                     f'{path_root}/250219_all_combined')
    # 将合并后的内容写入新的文件中


if __name__ == "__main__":
    main()
