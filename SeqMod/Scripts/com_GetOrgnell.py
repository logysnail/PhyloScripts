"""生成GetOrganell的命令，一行一个"""


import FileOperate


file_path = FileOperate.get_list("../Import/list.txt")
commands = []
for index in range(0, 54, 2):
    p1 = file_path[index].split(",")[0]
    p2 = file_path[index + 1].split(",")[0]
    name = file_path[index + 1].split(",")[1]
    sp = file_path[index + 1].split(",")[2]
    command = f'nohup python /chenlab/yujinren/software/GetOrganelle-1.7.1/get_organelle_from_reads.py' \
              f' -1 {p1} -2 {p2} -o {name},' \
              f'-R 15 -k 21,45,65,85,105 -F embplant_pt\t{name}\t{sp}'
    commands.append(command)
FileOperate.write_list(commands, "../Output/GetOrganellecommands_250402.txt")
