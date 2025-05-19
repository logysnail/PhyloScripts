"""
匹配内容 a-1,b-2,c-3
输入
a
a
c
c
b
输出
a,1
a,1
c,3
c,3
b,2
"""

import FileOperate

state_path = "../Config/state.txt"
list_path = "../Import/list.txt"
out_file_path = "../Output/code_state.txt"


dic = {}
with open(state_path, "r", encoding='utf-8') as state_file:
    records = state_file.readlines()
    for record in records:
        code = record.strip().split(",")[0]
        state = record.strip().split(",")[1]
        dic[code] = state

ls = FileOperate.get_list(list_path)
with open(out_file_path, "w", encoding='utf-8') as out_file:
    for ele in ls:
        if ele in dic:
            out_file.write(f'{ele}\t{dic[ele]}\n')
        else:
            out_file.write(f'{ele}\t \n')

