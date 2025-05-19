

import FileOperate


def filter_lines(file_1, file_2, output_folder, chose):
    """筛选没有file2内条目的file1条目"""
    list_1 = FileOperate.get_list(file_1)
    list_2 = FileOperate.get_list(file_2)
    f_1 = FileOperate.get_file_name(file_1)[0]
    f_2 = FileOperate.get_file_name(file_2)[0]
    if chose == "noin":
        rested_list = [line for line in list_1 if not any(number in line for number in list_2)]
        FileOperate.write_list(rested_list, f'{output_folder}/{f_1}_remove_{f_2}.txt')
    if chose == "in":
        rested_list = [line for line in list_1 if any(number in line for number in list_2)]
        FileOperate.write_list(rested_list, f'{output_folder}/{f_1}_remove_{f_2}.txt')


def main(import_folder, config_folder, output_folder):
    FileOperate.loop_folder_2(filter_lines, import_folder, config_folder, output_folder=output_folder, chose="noin")


if __name__ == '__main__':
    main("../Import",
         "../Config",
         "../Output")
