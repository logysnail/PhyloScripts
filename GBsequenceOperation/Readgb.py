"""read the gb file with sequence undivided"""
import re


def divide_gb(gb_lines):
    """每条记录作为元素形成列表"""
    record_list = []
    record = []
    for line in gb_lines:
        if line == "//":
            record_list.append(record)
            record = []
        else:
            record.append(line)
    return record_list


def match_line_begin(target, origin_record):
    for line in origin_record:
        match = re.match(target, line)
        if match:
            return line.replace(target, "")


def clean_gb_seq(sequence_lines):
    """gb文件里的序列改成一行"""
    seq = ""
    for line in sequence_lines:
        clean_line = re.sub('[\d\s]', "", line)
        seq = seq + clean_line.replace("ORIGIN", "")
    return seq


def feature_and_origin(origin_record):
    """读取记录的基因名以及原始序列"""
    is_feature_line = False
    is_origin_line = False
    ls_gene_name = []
    sequence_lines = []
    for line in origin_record:
        if re.match('ORIGIN', line):
            is_origin_line = True
        if is_origin_line:
            sequence_lines.append(line)
    seq = clean_gb_seq(sequence_lines)
    # 序列以及序列长度
    for line in origin_record:
        if re.match('FEATURES', line):
            is_feature_line = True
        if re.match('ORIGIN', line):
            is_feature_line = False
        if is_feature_line:
            find_gene_name = re.findall('/gene="(.+)"', line)
            if find_gene_name:
                # 如果是没有记录的基因名加入列表
                gene_name = find_gene_name[0]
                if gene_name not in ls_gene_name:
                    ls_gene_name.append(gene_name)
    return ls_gene_name, seq


def extract_records_info(origin_record):
    # 反复调用函数匹配需要的行,整理数据
    ACCESSION = match_line_begin("ACCESSION   ", origin_record)
    ORGANISM = match_line_begin("  ORGANISM  ", origin_record)
    genes_seq = feature_and_origin(origin_record)
    ls_gene = genes_seq[0]
    genes = ""
    for gene in ls_gene:
        genes = genes + "/" + gene.replace(",", " ")
    seq = genes_seq[1].upper()
    record_line = f'{ORGANISM},{ACCESSION},{genes[1:]},{len(seq)},{seq}'
    return record_line


def summary_undivided_gb(record_lines):
    record_list = divide_gb(record_lines)
    summary_list = []
    for record in record_list:
        one_summary = extract_records_info(record)
        summary_list.append(one_summary)
    return summary_list
