import pandas
import pandas as pd
import os
import SeqOperate

"""根据geneious导出的gene位置表格，以及fasta文件，提取间区"""


# 注意geneious的导出数字格式不正常，有><符号，注意处理

def process_gene_intervals(df):
    for col in ['Minimum', 'Maximum']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

    # 2. 按 seq_name 分组，并按 min 排序
    df = df.sort_values(by=['Sequence Name', 'Minimum'])

    # 3. 初始化结果列表
    result = []

    # 4. 按 seq_name 分组处理
    for seq_name, group in df.groupby('Sequence Name'):
        # 如果组内只有一行，无法计算间隔，跳过
        if len(group) < 2:
            continue

        # 获取当前组的行
        group = group.reset_index(drop=True)

        # 5. 遍历相邻行，计算间隔
        for i in range(len(group) - 1):
            gene1 = group.loc[i, 'Name'].replace(" gene", "")
            gene2 = group.loc[i + 1, 'Name'].replace(" gene", "")
            inter_name = f"{gene1}-{gene2}"
            min_val = group.loc[i, 'Maximum']
            max_val = group.loc[i + 1, 'Minimum']

            # 添加到结果列表
            result.append({
                'seq_name': seq_name,
                'inter_name': inter_name,
                'min': min_val,
                'max': max_val
            })

    # 6. 将结果转换为 DataFrame
    result_df = pd.DataFrame(result, columns=['seq_name', 'inter_name', 'min', 'max'])
    # 过滤掉重复的 inter_name（不区分 gene1-gene2 和 gene2-gene1）
    result_df['sorted_inter_name'] = result_df['inter_name'].apply(lambda x: '-'.join(sorted(x.split('-'))))
    result_df = result_df.drop_duplicates(subset=['seq_name', 'sorted_inter_name']).drop(columns=['sorted_inter_name'])

    return result_df


def generate_inter_fasta_files(output_dir, df, fasta_dict):
    """
    生成以 inter_name 命名的 FASTA 文件。

    参数：
    - output_dir: str, 保存 FASTA 文件的文件夹路径
    - df: DataFrame, process_gene_intervals(df) 的输出结果
    - fasta_dict: 键为 seq_name，值为序列字符串
    """
    # 确保输出目录存在，如果不存在则创建
    os.makedirs(output_dir, exist_ok=True)

    # 遍历 DataFrame 的每一行
    for index, row in df.iterrows():
        seq_name = row['seq_name']
        inter_name = row['inter_name']
        min_val = row['min']
        max_val = row['max']

        # 从 fasta_dict 中获取对应的序列
        if seq_name in fasta_dict:
            sequence = fasta_dict[seq_name]
            # 提取子序列（Python 字符串索引从 0 开始，所以 min_val - 1）
            # min_val 到 max_val 是包含两端的，所以用 min_val-1 到 max_val
            print(seq_name, inter_name)
            print(min_val, max_val)
            min_val = int(min_val)
            max_val = int(max_val)
            sub_sequence = sequence[min_val - 1:max_val]

            # 生成 FASTA 文件路径
            fasta_file = os.path.join(output_dir, f"{inter_name}.fasta")

            # 写入 FASTA 文件
            with open(fasta_file, 'a') as f:
                f.write(f">{seq_name}\n{sub_sequence}\n")
        else:
            print(f"Warning: seq_name '{seq_name}' not found in fasta_dict, skipping {inter_name}")


def process_to_inter_fasta(csv_path, fasta_path, output_dir):
    """
    整合处理表格、读取 FASTA 并生成 inter_name FASTA 文件。

    参数：
    - df: DataFrame, 包含 seq_name, gene_name, min, max, direction 的原始表格
    - fasta_path: str, FASTA 文件路径
    - output_dir: str, 输出 inter_name FASTA 文件的目录
    """
    # 步骤 1: 处理表格生成间隔
    inter_df = process_gene_intervals(pandas.read_csv(csv_path))

    # 步骤 2: 读取 FASTA 文件为字典
    fasta_dict = SeqOperate.get_matrix_dic(fasta_path)

    # 步骤 3: 生成 inter_name 的 FASTA 文件
    generate_inter_fasta_files(output_dir, inter_df, fasta_dict)

    print(f"Processing complete. Inter-sequence FASTA files saved to {output_dir}")


def process_multiple_groups(csv_folder, fasta_folder, output_dir):
    """
    处理多个类群的表格和 FASTA 文件，生成 inter_name FASTA 文件到对应类群文件夹。

    参数：
    - csv_folder: csv存储的路径
    - fasta_folder: str, FASTA 文件所在目录，文件名需与类群名一致（如 group1.fasta）
    - output_base_dir: str, 输出基础目录，最终文件会存到 output_base_dir/类群名/
    """
    for file_name in os.listdir(csv_folder):
        group_name = file_name.replace(".csv", "")
        csv_path = os.path.join(csv_folder, f"{group_name}.csv")
        # 构建 FASTA 文件路径
        fasta_path = os.path.join(fasta_folder, f"{group_name}.fasta")

        # 确保 FASTA 文件存在
        if not os.path.exists(fasta_path):
            print(f"找不到 {fasta_path}，跳过 {group_name}")
            continue
        # 构建输出目录
        group_dir = os.path.join(output_dir, group_name)
        # 调用已有函数处理单个类群
        print(f"正在处理 {group_name}...")
        process_to_inter_fasta(csv_path, fasta_path, group_dir)


def main():
    csv_folder = "../Config"
    fasta_folder = "../Import"
    output_dir = "../Output"
    process_multiple_groups(csv_folder, fasta_folder, output_dir)


if __name__ == "__main__":
    main()
