"""保留想要的序列"""
import FileOperate
import SeqOperate as so


def write_extract(seq_fasta_path, name_list_path):
    # seq_matrix = so.extract_seqs(name_list_path, seq_fasta_path)
    seq_matrix = so.remove_include(name_list_path, seq_fasta_path)
    # n = FileOperate.get_file_name(name_list_path)
    # s = FileOperate.get_file_name(seq_fasta_path)
    out_path = seq_fasta_path.replace("Import", "Output")
    # so.rmix(f'{out_path}/{s[0]}_{n[0]}.fasta', seq_matrix)
    so.rmix(out_path, seq_matrix)


def loop_fam(folder_path, name_list_path):
    fam_out = folder_path.replace("Import", "Output")
    FileOperate.makedir(fam_out)
    FileOperate.loop_folder_1(write_extract, folder_path, name_list_path=name_list_path)


def main():
    # out_path = "../seq"
    # seq_path = "../Originseq"
    # list_path = "../SpList"
    # fo.makedir(out_path)
    # fo.loop_folder_2(write_extract, seq_path, list_path, out_path=out_path)

    input_folder = "E:/py/SeqMod/Import"
    name_list_path = "../Config/to_remove.txt"
    FileOperate.loop_folder_1(loop_fam, input_folder, name_list_path=name_list_path)


if __name__ == "__main__":
    main()
