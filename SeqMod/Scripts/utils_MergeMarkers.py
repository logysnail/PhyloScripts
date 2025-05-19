"""把一个文件夹下数个二级文件夹之间的同名文件
的内容合并到一个文件，放入一个新的文件夹"""
import re
import FileOperate
import os
from Bio import SeqIO

import re


def extract_hyphenated_words(text):
    # 匹配包含连字符的单词
    hyphenated_words = re.findall(r'\b\w+-\w+\b', text)
    # 将匹配到的单词以空格连接返回
    if hyphenated_words:
        return ' '.join(hyphenated_words)
    else:
        return 'cp'


def test_file(file_path, output_folder, family_name):
    """如果这个文件名已经出现过，
    则把内容加到现有文件中
    如果没有出现过
    则复制一个到输出文件夹"""
    file_name = os.path.basename(file_path)
    file_content = FileOperate.read_file(file_path)
    # file_content = file_content.replace('>', f'>{family_name}%')
    # file_name = extract_hyphenated_words(file_name) + ".fasta"
    exist = os.path.isfile(os.path.join(output_folder, file_name))

    if exist:
        with open(f'{output_folder}/{file_name}', 'a') as file:
            file.write(file_content.replace("|", "%"))
    else:
        with open(f'{output_folder}/{file_name}', 'x') as file:
            file.write(file_content.replace("|", "%"))


def read_folders(folder_path, output_folder):
    FileOperate.makedir(output_folder)
    fam_name = os.path.basename(folder_path)
    FileOperate.loop_folder_1(test_file, folder_path, output_folder=output_folder, family_name=fam_name)


def combine_files(folders_path):
    """
    合并数个文件夹内文件名一样的内容
    放置在“路径+combined”
    :param folders_path: 文件夹所处的路径
    :return: 无
    """
    output = f'{folders_path}_combined'
    FileOperate.makedir(output)
    FileOperate.loop_folder_1(read_folders, folders_path, output_folder=output)


def main():
    input_folder = "E:/Global_mega_diversification/SequenceData/Data_NCBI/cp/整合cds和间区"
    FileOperate.loop_folder_1(combine_files, input_folder)


if __name__ == '__main__':
    main()
