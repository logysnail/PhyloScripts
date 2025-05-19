import os
import SeqOperate
import FileOperate

"""输出目录下各个二级目录内所有序列的物种名"""


def get_sp_list(import_folder, output_folder):
    """遍历文件夹内的所有文件，读取后返回所有键值到列表"""
    ls = []
    for folder_name in os.listdir(import_folder):
        folder_path = f'{import_folder}/{folder_name}'
        for file_name in os.listdir(folder_path):
            file_path = f'{folder_path}/{file_name}'
            dic = SeqOperate.get_matrix_dic(file_path)
            for key in dic:
                ls.append(key)
    ls = list(set(ls))
    FileOperate.write_list(ls, f'{output_folder}/sp.txt')


def main():
    import_folder = "../Import"
    output_folder = "../Output"
    get_sp_list(import_folder, output_folder)


if __name__ == '__main__':
    main()
