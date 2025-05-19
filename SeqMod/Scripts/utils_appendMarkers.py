import os
"""
合并文件夹1内的文件与文件夹2内和文件夹1同名的文件，输出到文件夹3
"""

def merge_files(folder1, folder2, folder3):
    # 确保目标文件夹3存在，如果不存在则创建
    if not os.path.exists(folder3):
        os.makedirs(folder3)
    # 遍历文件夹1中的所有文件
    for filename in os.listdir(folder1):
        file1_path = os.path.join(folder1, filename)
        # 确保是文件而不是子目录
        if os.path.isfile(file1_path):
            file2_path = os.path.join(folder2, filename)
            file3_path = os.path.join(folder3, filename)
            # 检查文件夹2中是否有同名文件
            if os.path.isfile(file2_path):
                try:
                    # 读取文件夹1和文件夹2中的文件内容
                    with open(file1_path, 'r', encoding='utf-8') as f1:
                        content1 = f1.read()
                    with open(file2_path, 'r', encoding='utf-8') as f2:
                        content2 = f2.read()
                    # 合并内容
                    merged_content = content1 + "\n" + content2
                    # 将合并后的内容写入文件夹3中
                    with open(file3_path, 'w', encoding='utf-8') as f3:
                        f3.write(merged_content)
                    print(f"文件 '{filename}' 已合并并保存到 '{file3_path}'")
                except Exception as e:
                    print(f"处理文件 '{filename}' 时发生错误: {e}")
            else:
                print(f"文件夹2中找不到文件 '{filename}'，跳过该文件。")
        else:
            print(f"'{filename}' 不是文件，跳过该项。")


# 调用示例
folder1 = 'E:/Global_mega_diversification/SequenceData/Data_NCBI/cp/geneious提取cds/fams_rename_longest'
folder2 = 'path_to_folder2'
folder3 = 'E:/Global_mega_diversification/SequenceData/Data_NCBI/cp/geneious提取cds/fams_append_more'

merge_files(folder1, folder2, folder3)
