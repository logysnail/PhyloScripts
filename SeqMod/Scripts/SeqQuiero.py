import os
import FileOperate as fo
import SeqOperate as so


def write_extract(name_list_path, seq_fasta_path, out_path):
    seq_matrix = so.extract_seqs(name_list_path, seq_fasta_path)
    n = fo.get_file_name(name_list_path)
    s = fo.get_file_name(seq_fasta_path)
    so.rmix(f'{out_path}/{s[0]}_{n[0]}.fasta', seq_matrix)


def main():
    out_path = "../seq"
    seq_path = "../Originseq"
    list_path = "../SpList"
    fo.makedir(out_path)
    fo.loop_folder(fuc=write_extract, fold_1=seq_path, fold_2=list_path, out_path=out_path)


if __name__ == "__main__":
    main()
