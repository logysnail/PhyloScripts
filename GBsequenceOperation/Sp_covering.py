import os
import seqmoder

import Readgb


def write_sampling_file(in_path, out_path):
    all_sp = []
    for taxon_dir in os.listdir(in_path):
        taxon_path = f'{in_path}{taxon_dir}/'
        dic_marker_sampling = marker_sampling_dic(taxon_path)
        ls_sp = []
        marker_ls = []
        for marker in dic_marker_sampling:
            marker_ls.append(marker)
            for sp in dic_marker_sampling[marker]:
                ls_sp.append(sp)
        sps = list(set(ls_sp))
        all_sp = all_sp + sps
        with open(f'{out_path}{taxon_dir}.csv', "w") as matrix_file:
            matrix_file.write("species")
            for marker in marker_ls:
                matrix_file.write(f',{marker}')
            matrix_file.write(f'\n')
            for sp in sps:
                matrix_file.write(f'{sp}')
                for marker in marker_ls:
                    dic_sp_acc = dic_marker_sampling[marker]
                    if sp in dic_sp_acc:
                        # 物种在marker有取样
                        acc = dic_sp_acc[sp]
                        matrix_file.write(f',{acc}')
                    else:
                        matrix_file.write(f',-')
                matrix_file.write(f'\n')
    return all_sp


def marker_sampling_dic(all_path):
    """获得取样的marker：acc字典"""
    dic_marker_sampling = {}
    for file in os.listdir(all_path):
        marker = file.split(".")[0]
        if marker == 'cp':
            sample_acc = extract_cp(f'{all_path}{file}')
        else:
            sample_acc = extract_sp_list(f'{all_path}{file}')
        if sample_acc:
            dic_marker_sampling[marker] = sample_acc
    return dic_marker_sampling


def extract_sp_list(path):
    """筛选符合条件的marker的序列
    返回这个sp:acc的字典"""
    marker_matrix = seqmoder.get_matrix_dic(path)
    sampled = {}
    if len(marker_matrix) > 10:
        for sample in marker_matrix:
            sp = sample.split("%")[0]
            acc = sample.split("%")[1]
            seq = marker_matrix[sample]
            seq_len = len(seq)
            if seq_len > 30:
                sampled[sp] = acc
    else:
        return False
    return sampled


def extract_cp(path):
    sampled = {}
    records = Readgb.divide_gb(seqmoder.get_list(path))
    for record in records:
        ORGANISM = Readgb.match_line_begin("  ORGANISM  ", record)
        ACCESSION = Readgb.match_line_begin("ACCESSION   ", record)
        sampled[ORGANISM] = ACCESSION
    return sampled


summary_path = "./gb_summary/"
split_seq_path = f'{summary_path}Cp_and_marker_NCBI/'
sampling_path = f'{summary_path}Sampling_matrix/'
seqmoder.makedir(sampling_path)
all_sampling = write_sampling_file(split_seq_path, sampling_path)
with open("all_NCBI_SP.TXT", "w") as ncbi_sp_file:
    for nbci_sp in all_sampling:
        ncbi_sp_file.write(f'{nbci_sp}\n')
