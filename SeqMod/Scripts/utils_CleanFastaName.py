import os
import re

"""整理序列名并且合并同名的文件"""


def clean_filename(filename):
    match = re.search(r'(\S+-[A-Za-z]+)', filename)
    if match:
        print(match.group(0))
        return match.group(0) + '.fasta'  # 返回匹配的字符串（如 rpl20-rps12）
    else:
        return filename  # 如果没有找到匹配的部分，返回 None


def merge_files_in_directory(directory, out):
    # 获取目录下的所有文件
    files = os.listdir(directory)
    os.mkdir(out)
    # 用于记录已处理的文件名（去掉"-XXX"部分后的名字）
    merged_files = {}
    for file in files:
        # 如果是fasta文件
        if file.endswith('.fasta'):
            # 更新文件名
            cleaned_name = clean_filename(file)
            # 如果已经处理过同名文件，合并内容
            if cleaned_name in merged_files:
                with open(os.path.join(directory, file), 'r') as f:
                    content = f.read()
                merged_files[cleaned_name].append(content)
            else:
                # 否则创建一个新的合并内容列表
                with open(os.path.join(directory, file), 'r') as f:
                    content = f.read()
                merged_files[cleaned_name] = [content]

    # 将合并后的内容保存到新文件中
    for cleaned_name, content_list in merged_files.items():
        # 将多个文件的内容合并
        merged_content = ''.join(content_list)
        with open(os.path.join(out, cleaned_name), 'w') as f:
            f.write(merged_content)
        print(f"文件 {cleaned_name} 已合并并保存。")


def main():
    # 调用函数并传入目标目录路径
    directory = "E:/Global_mega_diversification/SequenceData/Data_NCBI/cp/脚本提取gb_cds_inter/GBs_summary_gene/vita_combined"  # 替换为实际目录
    out = "E:/Global_mega_diversification/SequenceData/Data_NCBI/cp/脚本提取gb_cds_inter/GBs_summary_gene/vita_cleaned"
    merge_files_in_directory(directory, out)


if __name__ == '__main__':
    main()
