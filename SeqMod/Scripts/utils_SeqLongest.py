import SeqOperate
import AlignmentOperate
import FileOperate

"""对于同名物种序列，挑选最长的那一个"""


def clean_matrix(align_path):
    """deal with the alignment"""
    seq_dic = SeqOperate.get_matrix_dic(align_path)
    new_seq_dic = {}
    sp_list = []
    for seq_name in seq_dic:
        species = seq_name.split("%")[1]
        sp_list.append(species)
    for sp in sp_list:
        max_len_seq = ""
        max_len = 0
        new_seq_name = ""
        for seq_name in seq_dic:
            species = seq_name.split("%")[1]
            if species == sp:
                seq_len = len(seq_dic[seq_name].strip("-").strip("N"))
                if seq_len > max_len:
                    max_len_seq = seq_dic[seq_name]
                    max_len = seq_len
                    new_seq_name = seq_name.replace("_R_", "")
                    new_seq_name = new_seq_name.replace("%", "|")
        if "_sp." in new_seq_name:
            continue
        else:
            new_seq_dic[new_seq_name] = max_len_seq
    try:
        SeqOperate.rmix(align_path.replace("Import", "Output"), new_seq_dic)
    except Exception as e:
        print(f"发生了一个错误: {e}")


def loop_fam(folder_path):
    fam_out = folder_path.replace("Import", "Output")
    FileOperate.makedir(fam_out)
    FileOperate.loop_folder_1(clean_matrix, folder_path)


def main():
    input_folder = "E:/py/SeqMod/Import"
    FileOperate.loop_folder_1(loop_fam, input_folder)


if __name__ == '__main__':
    main()
