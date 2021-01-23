import json
import pathlib
import numpy as np

if __name__ == '__main__':
    title = []
    data = []
    files = pathlib.Path('C:\\Users\\mi161303\\Desktop\\卒業研究\\MtG_AI\\data\\').glob("battle-base-mcts.csv")
    for file in files:
        f = open(file, 'r', encoding='UTF-8')
        txt = f.readlines()
    for i in range(txt.__len__()):
        txt[i] = txt[i].replace("\n", '')
    for i in range((int)(txt.__len__()/2)):
        title.append(txt[i*2])
        data.append(txt[i*2+1].split(','))
    for i in range(data.__len__()):
        for j in range(data[i].__len__()):
            data[i][j] = (int)(data[i][j])

    y = np.array([np.array(i).mean() for i in data])
    e = np.array([np.array(i).std() for i in data])

    for i in range(y.__len__()):
        print("(" + str(y[i]) + "," + str(e[i]) + ")")
