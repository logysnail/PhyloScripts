"""生成barcondefinder的下载命令"""


def file_to_dic(file, key_colum, value_colum):
    """
    根据表格里的两列数据生成一个字典
    :param file: 一个表格
    :param key_colum: 键所在列
    :param value_colum: 值所在列
    :return: 一个字典
    """
    dic = {}
    with open(file, 'r') as table:
        table_lines = table.readlines()
        for line in table_lines:
            line = line.strip().split(",")
            key = line[key_colum]
            value = line[value_colum]
            dic[key] = value
    return dic


def write_list(ls, file_path):
    """
    把列表逐行写入txt文件
    :param ls:列表
    :param file_path:文件路径
    :return:无
    """
    with open(file_path, "w") as file:
        for ele in ls:
            file.write(f'{ele}\n')


def write_command(taxa_file, command_file):
    """
    批量生成命令行，用于在命令行窗口运行
    :param taxa_file:
    :param command_file:
    :return:
    """
    dic = file_to_dic(taxa_file, 0, 0)
    command_ls = []
    for taxa in dic:
        tax_id = dic[taxa]
        p1 = "python -m BarcodeFinder -query txid"
        p2 = "[Organism:exp] AND (plants[filter] AND biomol_genomic[PROP] AND ddbj_embl_genbank[filter] AND " \
             "chloroplast[filter]) -out E:\Global_mega_diversification\ZYJ\\"
        p3 = " -no_divide"
        command = f'{p1}{tax_id}{p2}{taxa}{p3}'
        command_ls.append(command)
    write_list(command_file, command_ls)


if __name__ == '__main__':
    write_command("../taxa_to_download_YYC.csv", "../20231107_command_ZYJ.txt")
