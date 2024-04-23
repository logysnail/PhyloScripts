import os
import re

import Readgb
import seqmoder


# 读取marker记录
def accession_list(path):
    """获取marker-accession_number列表"""
    ls_acc = []
    lines = seqmoder.get_list(path)
    for line in lines:
        acc = line.split(",")[1]
        ls_acc.append(acc)
    return ls_acc


def taxon_accession_dic(path):
    """输入有记录的二级文件夹路径
    嵌套字典记录[类群-marker-accession_number列表]"""
    dic = {}
    for taxa in os.listdir(path):
        path_dir = f'{path}{taxa}/'
        dic_marker = {}
        for record_file_name in os.listdir(path_dir):
            marker_file_path = f'{path_dir}{record_file_name}'
            # 提取marker
            marker_name = record_file_name.replace(".csv", "")
            # accession number列表获取
            accessions = accession_list(marker_file_path)
            dic_marker[marker_name] = accessions
        dic[taxa] = dic_marker
    return dic


def gene_index(gene, record):
    """获取基因检索"""
    index_1 = 0
    index_2 = 0
    for i in range(len(record)):
        gene_record = f'/gene="{gene}"'
        line = record[i].upper()
        if gene_record.upper() in line:
            index_line = record[i - 1]
            head = "     gene            "
            test_if_gene = re.match(head, index_line)
            if test_if_gene:
                nums = re.findall(r'\d+', index_line)
                print(nums)
                print(index_line)
                if nums:
                    index_1 = int(nums[0]) - 1
                    index_2 = int(nums[1]) - 1
    return index_1, index_2


def acc_to_fasta(m, dic, records):
    """根据accession_number 在gb中提取
    形成字典 记录 marker:物种名_号：序列 """
    numbers = dic[m]
    dic_sp_seq = {}
    for num in numbers:
        for record in records:
            ACCESSION = Readgb.match_line_begin("ACCESSION   ", record)
            if ACCESSION == num:
                ORGANISM = Readgb.match_line_begin("  ORGANISM  ", record)
                seq = Readgb.feature_and_origin(record)[1]
                print(ACCESSION + m)
                try:
                    # 可能序列只有1bp因此try
                    index = gene_index(m, record)
                    m_seq = seq[index[0]:index[1]]
                except:
                    m_seq = ""
                seq_name = f'{ORGANISM}%{ACCESSION}'
                dic_sp_seq[seq_name.replace(" ", "_")] = m_seq.upper()
    return dic_sp_seq


def acc_to_gb(m, dic, records):
    numbers = dic[m]
    ls = []
    for num in numbers:
        for record in records:
            ACCESSION = Readgb.match_line_begin("ACCESSION   ", record)
            if ACCESSION == num:
                ls = ls + record + ["//\n"]
    return ls


def acc_to_seqfile(dic, records):
    """每个marker的记录"""
    dic_marker = {}
    for m in dic:
        if m == "cp":
            x = acc_to_gb(m, dic, records)
        else:
            x = acc_to_fasta(m, dic, records)
        dic_marker[m] = x
    return dic_marker


def extract_seq_file(dic, path_in, path_out):
    """读取gb提取序列"""
    for taxa_name in dic:
        dic_marker_accession = dic[taxa_name]
        # 打开此类群的gb文件获取记录
        gb_file_path = f'{path_in}{taxa_name}/GenBank/sequence.gb'
        gb_records = Readgb.divide_gb(seqmoder.get_list(gb_file_path))
        out_dir = f'{path_out}{taxa_name}/'
        # 创建类群的文件夹
        seqmoder.makedir(out_dir)
        marker_file = acc_to_seqfile(dic_marker_accession, gb_records)
        for marker in marker_file:
            # 写入同名marker文件
            split_seq_file = f'{out_dir}{marker}'
            if marker == "cp":
                with open(f'{split_seq_file}.gb', "w") as cp_file:
                    gb_list = marker_file[marker]
                    for ele in gb_list:
                        cp_file.write(f'{ele}\n')
            else:
                seqmoder.rmix(f'{split_seq_file}.fasta', marker_file[marker])


summary_path = "./gb_summary/"
split_record_path = f'{summary_path}Split_sequence_NCBI/'
split_seq_path = f'{summary_path}Cp_and_marker_NCBI/'
gb_path = "./gb_files/"
seqmoder.makedir(split_seq_path)
dic_taxa_marker_acc = taxon_accession_dic(split_record_path)
extract_seq_file(dic_taxa_marker_acc, gb_path, split_seq_path)
