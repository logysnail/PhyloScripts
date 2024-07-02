import os
import Readgb


def get_list(file_path):
    """输入打开的文件，获得删除前后换行符，输出一个每行作为一个元素的列表"""
    opened = open(file_path, "r", encoding="UTF-8")
    clean_lines = []
    for line in opened.readlines():
        line = line.strip("\n")
        clean_lines.append(line)
    opened.close()
    return clean_lines


def batch_summary_gb(all_file_path):
    os.makedirs(f'{all_file_path}_summary')
    for file in os.listdir(all_file_path):
        with open(f'{all_file_path}_summary/{file}.csv', "w") as summary_gb_file:
            try:
                gb_records = get_list(f'{all_file_path}/{file}/GenBank/sequence.gb')
                summary_list = Readgb.summary_undivided_gb(gb_records)
                for summary in summary_list:
                    summary_gb_file.write(f'{summary}\n')
            except:
                continue


if __name__ == '__main__':
    path = "../YYC"
    batch_summary_gb(path)
