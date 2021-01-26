import pathlib

import numpy as np

if __name__ == '__main__':
    title = []
    data = []
    files = pathlib.Path('C:\\Users\\mi161303\\Desktop\\卒業研究\\MtG_AI\\log\\').glob("lo.log")
    for file in files:
        f = open(file, 'r', encoding='UTF-8')
        txt = f.readlines()
    for i in range(txt.__len__()):
        txt[i] = txt[i].replace("\n", '')
    for i in range(txt.__len__()):
        data.append(txt[i].split(','))

    log = [0 for _ in range(data.__len__())]
    for i in range(data.__len__()):
        for j in range(data[i].__len__()):
            if data[i].__len__()-1 != j:
                log[i] += (int)(data[i][j])/4
            if data[i].__len__()-1 == j:
                print(log[i]/(data[i].__len__()-1)*100)