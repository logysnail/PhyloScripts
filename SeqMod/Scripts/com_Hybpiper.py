import FileOperate
"""Hybpiper命令"""

file_path = FileOperate.get_list("../Import/list.txt")
commands = []
for index in range(0, 628, 2):
    p1 = file_path[index].split(",")[0]
    p2 = file_path[index + 1].split(",")[0]
    name = file_path[index + 1].split(",")[1]
    command = f'hybpiper assemble -r {p1} {p2} -t_dna Vitaceae_target.fasta --bwa --cpu 10 --prefix {name},' \
              f'{file_path[index + 1]}'
    commands.append(command)
FileOperate.write_list(commands, "../Output/Hybpipercommands_250121.txt")
