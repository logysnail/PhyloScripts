	readgb.py 模块：读取gb文件
顺序使用：
1.BarcodeFinder_command.py 生成命令行批量下载序列
2.Batch_summary_gb.py 批量整理下载的序列
3.Count_summary.py 读取并生成整理完的序列统计表
4.Clean_sampling.py 读取步骤2文件，分离不同marker的序列放入独立文件，保留相同片段最长序列
5.Sequence_file_extract.py 根据脚本4结果记录中的marker名以及accession number获取对应序列，创建同名fasta文件， cp是带注释的gb文件
6.Sp_covering.py 筛选物种取样够多且序列够长的marker 输出筛选marker + cp取样的物种取样表
