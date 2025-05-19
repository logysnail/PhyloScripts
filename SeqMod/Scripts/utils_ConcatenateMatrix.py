import re
import os
import pandas
import AlignmentOperate
import FileOperate

"""生成一个联合矩阵，并且给出分区"""


def generate_partition(out_dir, file_dir, marker_align_dic):
    start = 0
    parts = []
    with open(f'{out_dir}/{os.path.basename(file_dir)}.cfg', 'w') as cfg_file:

        #cfg_file.write('alignment = infile.phy;\n'
        #               'branchlengths = linked;\n'
        #               'models= GTR, GTR+G, GTR+I+G;\n'
        #               'model_selection = aicc;\n[data_blocks]\n')
        cfg_file.write('#nexus\n'
                       'begin sets;\n')
        for marker in marker_align_dic:
            print(marker)
            align = marker_align_dic[marker]
            parts.append(align)
            length = len(align)
            end = start + length
            cfg_file.write(f'	charset {marker}={start + 1}-{end};\n')
            start = end
        cfg_file.write('end;')
    main_df = pandas.concat(parts, axis=0, join='outer', ignore_index=True).fillna('?')
    return main_df


def concatenate_fasta(file_dir):
    out_dir = file_dir.replace('Import', 'Output')
    FileOperate.makedir(out_dir)
    marker_align_dic = {}
    sampling_df = pandas.DataFrame()
    for file_name in os.listdir(file_dir):
        # filename is same as marker
        align = AlignmentOperate.read_fasta_as_df(f'{file_dir}/{file_name}')
        for col in align.columns:
            # sequence name
            name = col.split('|')
            acc = name[2]
            align.rename(columns={col: f'{name[0]}|{name[1]}'}, inplace=True)
            sampling_df.loc[f'{name[0]}%{name[1]}', file_name] = acc
            sampling_df = sampling_df.copy()
        file_name = file_name.replace('.fasta', "")
        marker_align_dic[file_name] = align
    main_df = generate_partition(out_dir, file_dir, marker_align_dic)  # generate partition file
    fasta = AlignmentOperate.turn_df_as_fasta(main_df)
    FileOperate.rmix(f'{out_dir}/{os.path.basename(file_dir)}.fasta', fasta)
    sampling_df.to_csv(f'{out_dir}/{os.path.basename(file_dir)}.sample', ',')


def main():
    import_dir = "../Import"
    FileOperate.loop_folder_1(concatenate_fasta, import_dir)


if __name__ == "__main__":
    main()
