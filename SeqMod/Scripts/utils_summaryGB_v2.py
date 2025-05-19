"""读取整理gb文件（不完善）"""

import os
import FileOperate
import re


def divide_gb(gb_file):
    """每条记录作为元素形成列表"""
    record_list = []
    record = []
    gb_records = FileOperate.get_list(gb_file)
    for line in gb_records:
        if line == "//":
            record_list.append(record)
            record = []
        else:
            record.append(line)
    return record_list


def get_gb_seq(gb_record):
    is_origin_line = False
    sequence_lines = []
    for line in gb_record:
        if re.match('ORIGIN', line):
            is_origin_line = True
        if is_origin_line:
            sequence_lines.append(line)
    seq = ""
    for line in sequence_lines:
        clean_line = re.sub('[\d\s]', "", line)
        seq = seq + clean_line.replace("ORIGIN", "")
    return seq


def get_seq_range(line):
    nums = re.findall(r'\d+', line)
    if len(nums) == 2:
        index_1 = int(nums[0]) - 1
        index_2 = int(nums[1]) - 1
        return [index_1, index_2]
    else:
        return None


def feature_and_origin(gb_record, target):
    """读取记录的基因名以及原始序列"""
    is_feature_line = False
    sp_name = ""
    acc = ""
    # 获取序列
    seq = get_gb_seq(gb_record)
    marker_seq = {}
    for line_index in range(len(gb_record)):
        line = gb_record[line_index]
        if re.match('FEATURES', line):
            is_feature_line = True
        if re.match('ORIGIN', line):
            is_feature_line = False
        if "  ORGANISM  " in line:
            sp_name = line.replace("  ORGANISM  ", "")
        if "ACCESSION" in line:
            acc = line.replace("ACCESSION   ", "")
        if is_feature_line:
            # 找到/note或者/gene
            find_marker_name = re.findall(f'/{target}="(.+)"', line)
            print(line)
            if find_marker_name:
                # 如果是没有记录的基因名加入列表
                marker_name = find_marker_name[0]
                seq_name = f'{marker_name}%{sp_name}%{acc}'
                if seq_name not in marker_seq:
                    index = get_seq_range(gb_record[line_index - 1])
                    if index is not None:
                        if index[1] - index[0] > 2:
                            marker_seq[seq_name] = seq[index[0]:index[1]]
    return marker_seq


def summary_gb_file(gb_file, target, fam_fasta_path):
    records = divide_gb(gb_file)
    fam_name = os.path.basename(gb_file).replace('.gb', "")
    for record in records:
        marker_seq = feature_and_origin(record, target)
        for seq in marker_seq:
            marker = seq.split('%')[0]
            sp_name = seq.split('%')[1]
            acc = seq.split('%')[2]
            seq_name = f'{fam_name}%{sp_name}%{acc}'
            seq_name = seq_name.replace(" ", "_")
            seq_name = seq_name.replace("_x_", "_×_")
            marker = marker.replace("/", "")
            marker = marker.replace("*", "")
            with open(f'{fam_fasta_path}/{marker}.fasta', 'a') as marker_file:
                marker_file.write(f'>{seq_name}\n{marker_seq[seq]}\n')


def main():
    """
    根据genebank文件 生成 科%种名%NCBI号码 命名的序列文件
    """
    path_of_gbs = "E:/Global_mega_diversification/SequenceData/Data_NCBI/cp/脚本提取gb_cds_inter/GBs"
    path_of_summary = f'{path_of_gbs}_summary_gene'
    FileOperate.makedir(path_of_summary)
    target = 'gene'
    for gb in os.listdir(path_of_gbs):
        gb_file = f'{path_of_gbs}/{gb}'
        fam_fasta_path = f'{path_of_summary}/{gb.replace(".gb", "")}'
        FileOperate.makedir(fam_fasta_path)
        summary_gb_file(gb_file, target, fam_fasta_path)


if __name__ == '__main__':
    main()
