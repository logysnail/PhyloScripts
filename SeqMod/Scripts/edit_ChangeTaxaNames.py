import re
import FileOperate
import SeqOperate
import os

"""按需求重命名序列的名字"""
def change_name(fasta_file, name_file):
    seq_dic = SeqOperate.get_matrix_dic(fasta_file)
    new_dic = {}
    name_list = FileOperate.get_list(name_file)
    name_dic = {}
    for ele in name_list:
        ele_pair = ele.split(",")
        name_dic[ele_pair[0]] = ele_pair[1]

    for seq_name in seq_dic:
        seq = seq_dic[seq_name]
        seq_name = seq_name.replace("_x_", "_×_")
        seq_name = seq_name.replace("oi閼辩荡", "i%")
        seq_name = seq_name.replace("_閼寸牎", "×_")
        seq_name = seq_name.replace(" ", "_")
        seq_name = seq_name.replace("_鑴砡", "×_")
        seq_name = seq_name.replace("_(nom._inval.)", "")
        name_set = seq_name.split("%")
        if name_set[1] in name_dic:
            new_name = f'{name_set[0]}%{name_dic[name_set[1]]}%{name_set[2]}'
            new_dic[new_name] = seq
        else:
            print(name_set[1])
            new_dic[seq_name] = seq
    SeqOperate.rmix(fasta_file.replace("Import", "Output"), new_dic)


def loop_change_name(import_dir, name_file):
    out_dir = import_dir.replace('Import', 'Output')
    FileOperate.makedir(out_dir)
    FileOperate.loop_folder_1(change_name, import_dir, name_file=name_file)


def main():
    import_dir = "../Import"
    list_path = "../Config/list.txt"
    FileOperate.loop_folder_1(loop_change_name, import_dir, name_file=list_path)


if __name__ == "__main__":
    main()
