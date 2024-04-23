import seqmoder
import os


def write_matrix_info(dic_sp_gene, file_path):
    """写入字典内容到文件中
        字典： 物种：{基因名：[[NCBI号, 序列长度], []]}"""
    gene_ls = []
    for sp in dic_sp_gene:
        gene_dic = dic_sp_gene[sp]
        for gene in gene_dic:
            gene_ls.append(gene)
    gene_set = set(gene_ls)
    gene_ls = list(gene_set)
    with open(file_path, "w") as result_file:
        result_file.write("sp,")
        for gene in gene_ls:
            result_file.write(f'{gene},')
        result_file.write("\n")
        for sp in dic_sp_gene:
            gene_dic = dic_sp_gene[sp]
            result_file.write(f'{sp.strip(" ")},')
            for gene in gene_ls:
                if gene in gene_dic:
                    gene_info = gene_dic[gene]
                    gene_sampling = ""
                    for ac_len in gene_info:
                        accession = ac_len[0]
                        seq_len = ac_len[1]
                        gene_sampling = gene_sampling + f'{accession}:{seq_len}/'
                    gene_sampling = gene_sampling.strip("/")
                    result_file.write(gene_sampling)
                result_file.write(",")
            result_file.write("\n")


def count_summary(all_summary_path):
    dic_taxa = {}
    for file in os.listdir(all_summary_path):
        records_info = seqmoder.get_list(f'{all_summary_path}/{file}')
        ls_sp = []
        for record in records_info:
            info = record.split(",")
            sp = info[0]
            if sp not in ls_sp:
                ls_sp.append(sp)
        # 获得物种列表
        dic_sp_gene = {}
        for sp in ls_sp:
            # 每个物种遍历
            dic_sp_gene[sp] = {}
            for record in records_info:
                info = record.split(",")
                record_sp = info[0]
                accession = info[1]
                seq_len = info[3]
                record_genes = info[2].split("/")
                if record_sp == sp:
                    dic_gene_acc_len = dic_sp_gene[sp]
                    for record_gene in record_genes:
                        if record_gene in dic_gene_acc_len:
                            # 如果已经收录此基因
                            dic_gene_acc_len[record_gene].append([accession, seq_len])
                        else:
                            gene_info = [accession, seq_len]
                            dic_gene_acc_len[record_gene] = [gene_info]
                else:
                    continue
        write_matrix_info(dic_sp_gene, f'{all_summary_path}/matrix_{file}')
        taxa_name = file.replace(".csv", "")
        sp_num = len(dic_sp_gene)
        sum_gene = 0
        for sp in dic_sp_gene:
            num_gene = len(dic_sp_gene[sp])
            sum_gene = sum_gene + num_gene
        if sp_num > 0:
            av_gene = sum_gene / sp_num
        else:
            av_gene = 0
        dic_taxa[taxa_name] = [sp_num, av_gene]

    with open(f'{all_summary_path}/取样率统计.csv', "w") as count_file:
        count_file.write("类群,取样物种数量,物种平均marker数量\n")
        for taxa in dic_taxa:
            count_file.write(f'{taxa},{dic_taxa[taxa][0]},{dic_taxa[taxa][1]}\n')


if __name__ == '__main__':
    path = "./YYC_summary"
    count_summary(path)
