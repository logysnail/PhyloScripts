"""
计算简约信息位点
"""

import os

path_all_file = "E:/py/matrix_mod/import"
files_1 = os.listdir(path_all_file)  # 读入一级文件夹
num1 = len(files_1)
result_file = open("E:/py/matrix_mod/cds_Pi_result.csv", "w")
result_file.write("filename" + "," + "sequencelenth" + "," + "简约信息位点个数" + "," + "\n")
for b in range(num1):  # 遍历所有二级文件夹
    matrix_file = open("E:/py/matrix_mod/import/" + files_1[b], "r")
    matrix = matrix_file.readlines()
    dic = {}
    for i in range(len(matrix)):
        if ">" in matrix[i]:
            sequence = matrix[i]
            key = sequence.strip("\n")
            key = key.strip(">")
            value = matrix[i + 1].strip("\n")
            dic[key] = value
    n = len(dic)  ## 统计序列数量n
    seqs = dic.keys()
    lenths = []
    for seq in seqs:
        ls = dic[seq]
        lenseq = len(ls)
        lenths.append(lenseq)
    ##找出最长序列
    seqlenth = max(lenths)
    S = 0  ##计算变异位点
    for a in range(seqlenth):
        cA = 0
        cT = 0
        cC = 0
        cG = 0
        cX = 0
        for seq in seqs:
            ls = dic[seq]
            bp = ls[a - 1]
            if bp == "A":
                cA = cA + 1
            if bp == "T":
                cT = cT + 1
            if bp == "C":
                cC = cC + 1
            if bp == "G":
                cG = cG + 1
            if bp == "-":
                cX = cX + 1
            if bp not in "ATCG-":
                print("error")
        #统计一个位点的碱基种类
        bp_num = [cA, cT, cG, cC]
        #单个位点碱基数列表
        if cX == 0:
            #判断是否有缺失
            if max(bp_num) == n:
                S = S
                #判断是否有变异
            else:
                bp_num.remove(max(bp_num))
                if any(i >= 2 for i in bp_num):
                    S = S + 1
                    #如果有多于2的碱基有效位点加1
        #计算有效位点数
    print(str(S))
    matrix_file.close()
    result_file.write(files_1[b] + "," + str(seqlenth) + "," + str(S) + "," + "\n")
result_file.close()
print("done")
