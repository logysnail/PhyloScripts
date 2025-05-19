"""
比对序列只保留snp位点
"""

import AlignmentOperate as ao
import FileOperate

def snp_align(align_path):
    df_align = ao.read_fasta_as_df(align_path)
    align = ao.Alignment(df_align)
    align.snp_cites()
    outfile_path = align_path.replace("Import", "Output")
    ao.write_df_fasta(align.alignment, outfile_path)


def loop_fam(folder_path):
    fam_out = folder_path.replace("Import", "Output")
    FileOperate.makedir(fam_out)
    FileOperate.loop_folder_1(snp_align, folder_path)


def main():
    input_folder = "E:/py/SeqMod/Import"
    FileOperate.loop_folder_1(loop_fam, input_folder)


if __name__ == '__main__':
    main()

