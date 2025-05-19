

import FileOperate
import AlignmentOperate
"""
把一个比对序列文件按照注释分割成几个marker
"""

def divide_marker(file_path, output_folder):
    file_name = FileOperate.get_file_name(file_path)
    FileOperate.makedir(f'{output_folder}/{file_name}')
    # create folder
    df = AlignmentOperate.read_fasta_as_df(file_path)
    alignment = AlignmentOperate.Alignment(df)



def main():
    file_path = "E:/py/SeqMod/Import/Vitaceae"
    output_folder = "E:/py/SeqMod/Output"
    index_file = "E:/py/SeqMod/Config/vitaceae_partition"
    divide_marker(file_path, output_folder)


if __name__ == '__main__':
    main()
