"""
合并文件夹里面a-b b-a 的间区文件
"""
import FileOperate
import os
import shutil


def merge_inter(input_folder, output_folder):
    # 获取 input_folder 中所有的文件名
    files = os.listdir(input_folder)
    merged_files = set()  # 用于记录已经合并过的文件对
    # 遍历 input_folder 中的文件
    for filename in files:
        # 检查是否是 a-b 格式的文件
        if '-' in filename:
            filename1 = filename.replace(".fasta", "")
            # 获取文件名的两个部分，假设文件格式为 a-b
            parts = filename1.split('-')
            if len(parts) == 2:
                a, b = parts
                # 检查 b-a 文件是否存在
                reverse_filename = f"{b}-{a}.fasta"
                if reverse_filename in files and filename not in merged_files and reverse_filename not in merged_files:
                    # 读取 a-b 文件和 b-a 文件的内容
                    with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file1, \
                            open(os.path.join(input_folder, reverse_filename), 'r', encoding='utf-8') as file2:
                        content1 = file1.read()
                        content2 = file2.read()

                        # 合并内容
                        merged_content = content1 + "\n" + content2

                    # 合并后的文件路径
                    merged_filename = f"{a}-{b}.fasta"

                    # 将合并后的内容写入到 output_folder
                    out_path = os.path.join(output_folder, merged_filename)
                    print(out_path)
                    with open(out_path, 'w', encoding='utf-8') as merged_file:
                        merged_file.write(merged_content)
                    # 标记这两个文件已经被合并
                    merged_files.add(filename)
                    merged_files.add(reverse_filename)

        else:
            with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                with open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as merged_file:
                    merged_file.write(content)


print("文件合并完成！")


def loop_fam(folder_path):
    fam_out = folder_path.replace("Import", "Output")
    FileOperate.makedir(fam_out)
    merge_inter(folder_path, output_folder=fam_out)


def main():
    input_folder = "E:/py/SeqMod/Import"
    FileOperate.loop_folder_1(loop_fam, input_folder)


if __name__ == '__main__':
    main()
