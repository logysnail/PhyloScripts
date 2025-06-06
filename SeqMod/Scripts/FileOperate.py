import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
"""常用的操作文件功能"""

def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content


def makedir(path):
    """
    :param path: 输入路径
    :return: 如果没有路径就创建此路径的文件夹，没有返回值
    """
    if not os.path.exists(path):
        os.mkdir(path)


def get_list(file_path):
    """输入打开的文件，获得删除前后换行符，输出一个每行作为一个元素的列表"""
    opened = open(file_path, "r", encoding="UTF-8")
    clean_lines = []
    for line in opened.readlines():
        line = line.strip("\n")
        clean_lines.append(line)
    opened.close()
    return clean_lines


def write_list(ls, file_path):
    """
    把列表逐行写入txt文件
    :param ls:列表
    :param file_path:文件路径
    :return:无
    """
    with open(file_path, "w", encoding="UTF-8") as file:
        for ele in ls:
            file.write(f'{ele}\n')


def get_file_name(file_path):
    """获取不带后缀的文件名以及路径"""
    file_name = os.path.basename(file_path)
    name = file_name.split(".")[0]
    return name, os.path.dirname(file_path)


def loop_folder_2(fuc, fold_1, fold_2, **kwargs):
    """
    对两个文件夹中的文件两两组合操作
    :param fuc: 对两个文件操作的函数
    :param fold_1: 文件夹1
    :param fold_2: 文件夹2
    :return:
    """
    for file_1 in os.listdir(fold_1):
        for file_2 in os.listdir(fold_2):
            fuc(f'{fold_1}/{file_1}', f'{fold_2}/{file_2}', **kwargs)


def loop_folder_1(fuc, fold, **kwargs):
    for file in os.listdir(fold):
        fuc(f'{fold}/{file}', **kwargs)



def process_directory(process_func, directory, thread, *args, **kwargs):
    """
    遍历文件夹，使用多线程处理每个文件。

    参数：
    - directory: 要遍历的文件夹路径
    - process_func: 对每个文件进行处理的函数
    - *args: 传递给 process_func 的其他位置参数
    - **kwargs: 传递给 process_func 的关键字参数
    """
    # 获取文件夹下所有文件路径
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # 创建一个线程池，指定最大线程数（根据需要调整 max_workers）
    with ThreadPoolExecutor(max_workers=thread) as executor:
        # 使用 map 方法将处理任务分配给线程池中的线程
        executor.map(lambda file_path: process_func(file_path, *args, **kwargs), file_paths)


def compare_two_list_diff(names_1, names_2, fuc):
    """输入打开文件1，2.根据功能返回列表1-2或1/2并集的列表"""
    ls = []
    if fuc == "-":
        ls = list(set(names_1) - set(names_2))
    if fuc == "*":
        for name_1 in names_1:
            write = False
            for name_2 in names_2:
                if name_2 in name_1:
                    write = True
            if write:
                ls.append(name_1)
    return ls


def merge_file(files_path, output_file_path):
    """输入文件存放目录，整合目录中文件的指定文件名的文件"""
    files = os.listdir(files_path)  # 读入一级文件夹
    files_count = len(files)
    cps = open(f'{output_file_path}', "x")
    for i in range(files_count):
        f = open(files_path + '/' + files[i], "r")
        file_content = f.read()
        cps.write(file_content)
        f.close()
    cps.close()


def name_name_dic(path):
    """输入文件路径。每一行逗号左key，逗号右是value
    输出此字典"""
    dic = {}
    dic_lines = get_list(path)
    for dic_line in dic_lines:
        code = dic_line.split(",")[0]
        name = dic_line.split(",")[1]
        dic[code] = name
    return dic


def count_ele(ls):
    """统计列表中每一元素出现次数，输出字典"""
    result = Counter(ls)
    return dict(result)


def nocasesens_ls(ls):
    """大小写不敏感规则删除重复列表元素
    但是保留大小写"""
    ls = list(set(ls))
    no_sens = []
    keep_ls = []
    for ele in ls:
        if ele.upper not in no_sens:
            keep_ls.append(ele)
            no_sens.append(ele.upper())
    return keep_ls


def rmix(file, matrix):
    """在输入文件里写入矩阵字典为fasta"""
    with open(file, "w", encoding='utf-8') as matrix_file:
        for key in matrix:
            matrix_file.write(f'>{key}\n{matrix[key]}\n')