import FileOperate as fo


def get_matrix_dic(path):
    """输入文件路径，输出一个序列名-序列的字典"""
    with open(path, "r") as seqs:
        lines = seqs.readlines()
        seq_name = {}
        for seq_in in range(len(lines)):
            if ">" in lines[seq_in]:
                seq_name[lines[seq_in].strip(">\n")] = lines[seq_in + 1].strip()
    return seq_name


def get_matrix_dic_list(path):
    """输入文件路径，输出一个序列名-序列列表化的字典"""
    with open(path, "r") as seqs:
        lines = seqs.readlines()
        seq_name = {}
        for seq_in in range(len(lines)):
            if ">" in lines[seq_in]:
                seq = lines[seq_in + 1].strip()
                seq_list = []
                for c in seq:
                    seq_list.append(c)
                seq_name[lines[seq_in].strip()] = seq_list
    return seq_name


def extract_seqs(name_list_path, seq_fasta_path):
    """
    按照文件内的名字获取想要的序列
    :param name_list_path: 名单文件
    :param seq_fasta_path: 序列fasta
    :return: 序列字典
    """
    name_list = fo.get_list(name_list_path)
    old_matrix = get_matrix_dic(seq_fasta_path)
    new_matrix = {}
    missing = name_list.copy()
    for name in name_list:
        if name in old_matrix:
            new_matrix[name] = old_matrix[name]
            missing.remove(name)
    if len(missing) > 0:
        n = fo.get_file_name(name_list_path)
        s = fo.get_file_name(seq_fasta_path)
        fo.write_list(missing, f'{n[1]}/missing{n[0]}_in_{s[0]}.txt')
    return new_matrix


def rmix(file, matrix):
    """在输入文件里写入矩阵字典"""
    with open(file, "w", encoding='utf-8') as matrix_file:
        for key in matrix:
            matrix_file.write(f'>{key}\n{matrix[key]}\n')


def longest(dic):
    """输出最长序列"""
    length = 0
    for key in dic:
        len_this = len(dic[key])
        if len_this > length:
            length = len_this
    print("矩阵长度：" + str(length))
    return length


def reverse_sequence(str_seq, sta_point, end_point):
    """输入想要翻转序列以及具体片段的开头碱基序号，结尾序号
    输出reverse complement sequence"""
    origin_seq = str_seq[sta_point:end_point]
    reversed_seq = origin_seq[::-1]
    complement_seq = ""
    for bp in reversed_seq:
        if bp == "A":
            bp = "T"
        if bp == "C":
            bp = "G"
        if bp == "G":
            bp = "C"
        if bp == "T":
            bp = "A"
        complement_seq.join(bp)
    return str_seq[:sta_point] + complement_seq + str_seq[end_point:]


def move_sequence(str_seq, sta_point, end_point, move_to_point, direction):
    """输入想移动的序列，输入移动片段开头结尾索引，以及插入点索引。输出移动处理后序列"""
    to_move_seq = str_seq[sta_point:end_point]
    if direction == "+":
        return str_seq[:sta_point] + str_seq[end_point:move_to_point] + to_move_seq + str_seq[move_to_point:]
    if direction == "-":
        return str_seq[:move_to_point] + to_move_seq + str_seq[move_to_point:sta_point] + str_seq[end_point:]


def oneline_seq(path):
    """输入文件路径，输出一个序列名-序列的字典"""
    with open(path, "r") as seqs:
        lines = seqs.readlines()
    number = len(lines)
    for i in range(number):  # 对读取的列表（每一行）操作以下内容
        a = lines[i]
        first_characteristic = a[0]
        if first_characteristic == ">":
            print("ok")
        else:
            lines[i] = lines[i].strip('\n')  # 去掉换行符
    for i in range(number):
        a = lines[i]
        try:
            first_characteristic = a[0]  # 检索到每行第一个字符
            # 做一个打印一个看出哪里断
            if first_characteristic == ">":  # 第一个字符是x的时候，上一行加换行符
                lines[i - 1] = lines[i - 1] + '\n'
            else:
                continue
        except:
            continue
    seq_name = {}
    for seq_in in range(len(lines)):
        if ">" in lines[seq_in]:
            seq_name[lines[seq_in].strip(">\n")] = lines[seq_in + 1].strip()
    return seq_name
