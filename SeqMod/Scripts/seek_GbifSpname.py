import os
import pandas as pd
"""
对包含命名人的物种名在POWO数据库中查询"""

# 定义处理CSV文件并提取去重的第二列值的函数
def extract_and_write_unique_column_values(directory, output_file):
    # 用于存储所有第二列的唯一值
    unique_values = set()

    # 遍历目录下的所有CSV文件
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):  # 只处理csv文件
            file_path = os.path.join(directory, filename)

            # 读取csv文件
            df = pd.read_csv(file_path)

            # 确保csv文件有至少2列
            if df.shape[1] >= 3:
                # 获取第二列的值，并去重
                second_column_values = df.iloc[:, 2].dropna().unique()

                # 将这些值添加到集合中，集合会自动去重
                unique_values.update(second_column_values)

    # 将去重后的值写入文件，每个值一行
    with open(output_file, 'w', encoding='utf-8') as f:
        for value in sorted(unique_values):  # 排序后写入（如果需要）
            f.write(str(value) + '\n')

            print(f"去重后的第二列值已经保存到 {output_file}")

            # 定义主函数


def main():
    # 设置目标目录路径和输出文件
    directory = 'E:/Global_mega_diversification/PlantData/GibifData/Step2'  # 这里修改为你的目录路径
    output_file = '../gbif_name.txt'

    # 调用处理函数
    extract_and_write_unique_column_values(directory, output_file)


# 程序入口
if __name__ == '__main__':
    main()
