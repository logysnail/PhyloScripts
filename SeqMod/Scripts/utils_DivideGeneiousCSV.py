"""按照geneious软件输出的序列和注释csv
分割出单独marker的fasta序列文件"""
import os
import FileOperate
import pandas
import SeqOperate


def divide_csv(csv_path, output_path):
    df = pandas.read_csv(csv_path)
    folder_name = os.path.basename(csv_path).replace(".csv", "")
    folder_path = f'{output_path}/{folder_name}'
    FileOperate.makedir(folder_path)
    df = df.drop_duplicates(subset=['Name', 'Sequence Name'])
    grouped = df.groupby('Name').agg({'Sequence': list, 'Sequence Name': list}).reset_index()
    for _, row in grouped.iterrows():
        # `_` 表示我们不需要索引，只需要行数据
        marker = row['Name'].replace(" CDS", "").replace("/", " ").replace("*", " ")  # 访问当前行的 'Name' 列
        dic = {}
        accs = row['Sequence Name']  # 访问当前行的 'Sequence Name' 列
        seqs = row['Sequence']  # 访问当前行的 'Seq' 列
        for acc, seq in zip(accs, seqs):
            dic[acc] = seq
        file_path = f'{folder_path}/{marker}.fasta'
        SeqOperate.rmix(file_path, dic)
    print(grouped)


def main():
    import_fold = "E:/py/SeqMod/Import"
    output_fold = "E:/py/SeqMod/Output"
    FileOperate.loop_folder_1(divide_csv, import_fold, output_path=output_fold)
    # 将合并后的内容写入新的文件中


if __name__ == "__main__":
    main()
