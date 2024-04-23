import bfop


def write_command(taxa_file, command_file):
    dic = bfop.file_to_dic(taxa_file, 0, 0)
    command_ls = []
    for taxa in dic:
        tax_id = dic[taxa]
        p1 = "python -m BarcodeFinder -query txid"
        p2 = "[Organism:exp] AND (plants[filter] AND biomol_genomic[PROP] AND ddbj_embl_genbank[filter] AND " \
             "chloroplast[filter]) -out E:\Global_mega_diversification\ZYJ\\"
        p3 = " -no_divide"
        command = f'{p1}{tax_id}{p2}{taxa}{p3}'
        command_ls.append(command)
    bfop.write_ls(command_file, command_ls)


if __name__ == '__main__':
    write_command("../taxa_to_download_YYC.csv", "../20231107_command_ZYJ.txt")
