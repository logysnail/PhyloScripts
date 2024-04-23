import os
import re
dic = ["rbcL", "rbcl"]
for mk in dic:
    os.mkdir(f'{mk}')
    with open(f'{mk}.csv', "w") as fi:
        print("ok")
