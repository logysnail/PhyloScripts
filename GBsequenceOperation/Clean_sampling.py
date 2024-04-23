import os
import seqmoder


def annotated_seq(lines):
    """获得有标记的序列"""
    ls_annotated = []
    for record in lines:
        marker = record.split(",")[2]
        if marker == "":
            continue
        else:
            ls_annotated.append(record)
    return ls_annotated


def split_whole_genome(lines):
    """分离可能是全叶绿体基因组的序列（长度大于150000bp)
    返回保留同种取样最长的全基因组序列记录 & 删除物种已有基因组记录的剩余记录"""
    ls_genome = []
    ls_rest = []
    genome_sp = []
    for record in lines:
        sp = record.split(",")[0]
        length = int(record.split(",")[3])
        if length >= 100000:
            ls_genome.append(record)
            genome_sp.append(sp)
        else:
            if sp in genome_sp:
                continue
            else:
                ls_rest.append(record)
    return remove_duplicate(ls_genome), ls_rest


def split_genome(lines):
    """分离剩下带有marker的基因
    每一个marker所有记录作为一个元素
    输出为字典 marker : 记录列表"""
    dic_marker_lines = {}
    ls_marker = []
    for line in lines:
        record_ls = line.split(",")
        markers = record_ls[2].split("/")
        for marker in markers:
            ls_marker.append(marker)
    # 所有的单个基因marker
    ls_marker = seqmoder.nocasesens_ls(ls_marker)
    for marker in ls_marker:
        records = []
        for line in lines:
            record_ls = line.upper().split(",")
            these_marker = record_ls[2].split("/")
            if marker.upper() in these_marker:
                records.append(line)
        dic_marker_lines[marker] = remove_duplicate(records)
    return dic_marker_lines


def remove_duplicate(lines):
    """删除记录中相同物种，保留序列更长的记录"""
    ls_sp = []
    for line in lines:
        record_ls = line.split(",")
        sp = record_ls[0]
        ls_sp.append(sp)
    ls_sp = list(set(ls_sp))
    record_sp_sp = []
    for sp in ls_sp:
        record_max_len = ""
        max_len = 0
        for line in lines:
            record_ls = line.split(",")
            r_sp = record_ls[0]
            length = int(record_ls[3])
            if r_sp == sp:
                if length > max_len:
                    max_len = length
                    record_max_len = line
                else:
                    continue
            else:
                continue
        record_sp_sp.append(record_max_len)
    return record_sp_sp


def write_records(path, lines):
    """写入筛选后的记录，格式不变"""
    with open(path, "w") as file:
        for line in lines:
            file.write(f'{line}\n')


file_path = "./gb_summary/sequence_NCBI"
new_dir = f'./gb_summary/Split_sequence_NCBI/'
seqmoder.makedir(new_dir)
for seq_file in os.listdir(file_path):
    print(seq_file)
    taxa_dir = f'{new_dir}{seq_file.replace(".csv", "")}/'
    # 每一个类群一个文件夹
    seqmoder.makedir(taxa_dir)
    file_lines = seqmoder.get_list(f'{file_path}/{seq_file}')
    annotated = annotated_seq(file_lines)
    # 输出全叶绿体基因组的序列
    full_genome_file = f'{taxa_dir}cp.csv'
    genome_single = split_whole_genome(annotated)
    records_genome = genome_single[0]
    write_records(full_genome_file, records_genome)
    # 分选剩下的
    records_single = genome_single[1]
    dic_marker = split_genome(records_single)
    for mk in dic_marker:
        write_records(f'{taxa_dir}{mk.replace("/", "_")}.csv', dic_marker[mk])
