import FileOperate
import AlignmentOperate
from collections import Counter
from Bio import Align

"""抠出序列比对不完善的一段，提高gap惩罚重新比对
提供筛选位点缺失率功能"""

aligner = Align.PairwiseAligner()

def merge_overlapping_ranges(dic):
    merged_dict = {}

    for key, intervals in dic.items():
        # Sort intervals by the starting index
        intervals.sort(key=lambda x: x[0])

        merged_intervals = []
        for current in intervals:
            # If merged_intervals is empty or current interval doesn't overlap with the last merged one
            if not merged_intervals or merged_intervals[-1][1] < current[0]:
                merged_intervals.append(current)
            else:
                # If the intervals overlap, merge them by updating the end index
                merged_intervals[-1] = (merged_intervals[-1][0], max(merged_intervals[-1][1], current[1]))

        merged_dict[key] = merged_intervals

    return merged_dict


def find_gap_region(df, max_gap_length):
    rows, cols = df.shape
    gap_regions = {col: [] for col in df.columns}
    # 第二步：为每个序列寻找符合条件的 gap 区域
    for col in df.columns:
        sequence = df[col].tolist()
        i = 0
        while i < rows:
            if sequence[i] == "-":
                # 找到连续 gap 的起点
                start = i
                while i < rows and sequence[i] == "-":
                    i += 1
                end = i - 1  # gap 结束位置
                gap_length = end - start + 1

                # 只保留长度 <= max_gap_length 的 gap
                if gap_length <= max_gap_length:
                    gap_regions[col].append((start, end))
            else:
                i += 1
    return gap_regions


def extend_gap(df, gap_regions, consensus, n):
    """
    向 gap 区域两端扩展，直到遇到连续 n 个非变异位点为止。

    参数：
    df: Pandas DataFrame，每列是一个序列，行是比对位置
    gap_regions: 字典，键是序列名，值是符合条件的 gap 区域列表 [(start, end), ...]
    consensus: 共识序列，用于判断变异位点
    n: 连续非变异位点的数量，默认值为 2

    返回：
    extended_regions: 字典，键是序列名，值是延伸后的 gap 区域列表 [(start, end), ...]
    """
    extended_regions = {col: [] for col in df.columns}

    # 遍历每个序列的 gap 区域
    for col, regions in gap_regions.items():
        for start, end in regions:
            # 获取当前序列的变异位点
            sequence = df[col]
            # 检查向两侧扩展的区域
            left, right = start, end

            # 向左延伸
            left_extension = None
            consecutive_non_variants = 0
            while left > 0:
                if sequence[left - 1] == consensus[left - 1]:
                    consecutive_non_variants += 1
                    left_extension = left - 1
                    if consecutive_non_variants >= n:
                        break
                else:
                    left_extension = left - 1
                    consecutive_non_variants = 0
                left -= 1

            # 向右延伸
            right_extension = None
            consecutive_non_variants = 0
            while right < len(sequence) - 1:
                if sequence[right + 1] == consensus[right + 1]:
                    consecutive_non_variants += 1
                    right_extension = right + 1
                    if consecutive_non_variants >= n:
                        break
                else:
                    right_extension = right + 1
                    consecutive_non_variants = 0
                right += 1

            # 计算延伸后的区间
            if left_extension is not None and right_extension is not None:
                new_start = left_extension
                new_end = right_extension
            elif left_extension is not None:
                new_start = left_extension
                new_end = end
            elif right_extension is not None:
                new_start = start
                new_end = right_extension
            else:
                new_start = start
                new_end = end

            # 如果延伸后的区间长度与原区间长度相同，说明没有有效延伸
            if new_end - new_start > end - start:
                extended_regions[col].append((new_start, new_end))

    return merge_overlapping_ranges(extended_regions)


def find_limited_gaps_and_regions(df, max_gap_length, n):
    """
    参数:
        df: Pandas DataFrame，每列是一个序列，行是比对位置
        max_gap_length: 连续 gap 的最大允许长度阈值
    返回:
        gap_regions: 字典，键是序列名，值是符合条件的 gap 区间列表 [(start, end), ...]
        extended_regions: 字典，键是序列名，值是从 gap 两端延伸后的区间列表 [(start, end), ...]
    """
    # 第一步：获取共识序列
    consensus = compute_consensus(df)

    # 第二步：为每个序列寻找符合条件的 gap 区域
    gap_regions = find_gap_region(df, max_gap_length)

    # 第三步：检查 gap 两端并向外延伸
    extended_regions = extend_gap(df, gap_regions, consensus, n)

    return extended_regions


def extract_operate_replace(df, intervals, func):
    """
    参数:
        df: Pandas DataFrame，每列是一个序列，行是比对位置
        intervals: 区间字典，例如 {'CPG01147': [(2990, 3284), (3486, 3516), (3923, 4856), (5928, 6095), (6207, 6404)],
    返回:
        modified_df: 修改后的 DataFrame
    """
    # 复制原始 DataFrame，避免修改原数据
    modified_df = df.copy()
    used_tip_int = []
    # 遍历每个区间
    for tip in intervals:
        for start, end in intervals[tip]:
            if (tip, intervals[tip]) in used_tip_int:
                continue
            # 提取当前区间的子 DataFrame
            region = modified_df.iloc[start:end + 1, :]
            original_length = region.shape[0]  # 记录原始长度
            # 提取 tip 在当前区间的子序列，并去掉 "-"
            tip_base = ''.join(region[tip]).replace("-", "").replace("n", "")
            # 找出所有与 tip 区域相同的其他列，去掉 "-" 后对比
            to_modify_cols = []  # 碱基相同的序列
            same_cols = []  # 完全相同的序列
            for col in region.columns:
                if ''.join(region[col]).replace("-", "").replace("n", "") == tip_base:
                    to_modify_cols.append(col)
                if region[col].equals(region[tip]):
                    same_cols.append(col)

            region = process_sequences(region, to_modify_cols, func)

            if region.shape[0] != original_length:
                raise ValueError(
                    f"操作后区间 ({start}, {end}) 长度从 {original_length} 变为 {region.shape[0]}，不符合要求")
            # 将操作后的结果放回原位置
            modified_df.iloc[start:end + 1] = region
            for col in to_modify_cols:
                used_tip_int.append((col, intervals[tip]))

    return modified_df


def compute_consensus(df):
    """
    计算给定 DataFrame 中的共识序列（每行碱基出现频率最多的碱基，排除 '-'）。
    """
    consensus = []
    # 遍历每一行，计算共识
    for idx, row in df.iterrows():
        # 获取该行的所有碱基，排除 '-'
        valid_bases = [base for base in row if base != '-']
        # 找出出现频率最高的碱基
        base_counts = Counter(valid_bases)
        most_common_base = base_counts.most_common(1)[0][0] if valid_bases else '-'
        consensus.append(most_common_base)
    return ''.join(consensus)


def process_sequences(df, tips, func):
    """
    处理序列，筛选出含有部分缺失的列，和共识比对后更新。

    参数：
    df: 需要处理的 DataFrame，包含多个序列。
    consensus: 共识序列，与每列进行比对。

    返回：
    更新后的 DataFrame。
    """
    # 步骤1：获取共识序列
    consensus = compute_consensus(df)
    # 步骤2：访问tip的序列，并且realign
    sequence = df[tips[0]]
    new_sequence = func(sequence, consensus)
    # 更新tip的序列
    for tip in tips:
        df.loc[:, tip] = list(new_sequence)  # 更新列为比对后的序列
    return df


def generate_alignments(target_seq, consensus):
    """
        使用 Biopython 进行序列比对，返回比对后的目标序列。

        参数:
        - target_seq: 目标序列，可能包含 '-'
        - consensus: 共识序列

        返回:
        - 比对后的目标序列
        """
    # 将列表转为字符串
    target_seq = ''.join(target_seq)
    # 调用 pairwise2 进行比对，允许空位（gap）并计算分数
    aligner.target_extend_gap_score = 0
    aligner.target_open_gap_score = -5
    aligner.query_open_gap_score = -10000.0
    aligner.query_extend_gap_score = -10000.0  # 保证比对序列维持原长
    alignments = aligner.align(target_seq, consensus)
    # 从比对结果中选取最佳的对齐
    best_alignment = alignments[0]
    print(best_alignment)
    # 返回对齐后的目标序列部分
    return best_alignment[0]


def del_sites(target_seq, consensus):
    return ''.join(len(target_seq) * "-")


def better_align(file_path):
    print("原始序列：", file_path)
    df = AlignmentOperate.read_fasta_as_df(file_path)  # 可选读取fasta还是phy
    # 可调节搜索gap的最大长度, 连续n个碱基配对成功就不再延伸重新比对范围，默认11。
    extended_regions = find_limited_gaps_and_regions(df, 1000, 6)
    # 对这些区域重新比对
    df = extract_operate_replace(df, extended_regions, generate_alignments)  # 可修改generate_alignments里面的惩罚参数
    #df = extract_operate_replace(df, extended_regions, del_sites)
    align = AlignmentOperate.Alignment(df)
    align.filter_site(0.95)  # 修剪一下序列
    df = align.alignment
    AlignmentOperate.write_df_fasta(df, file_path.replace("Import", "Output"))  # 输入路径改成输出路径


def loop_fam(folder_path):
    fam_out = folder_path.replace("Import", "Output")
    FileOperate.makedir(fam_out)
    FileOperate.loop_folder_1(better_align, folder_path)  # 指定线程，同时处理循环


def main():
    input_folder = "../Import"
    FileOperate.loop_folder_1(loop_fam, input_folder)


if __name__ == "__main__":
    main()
