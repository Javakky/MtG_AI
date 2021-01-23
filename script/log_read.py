import pathlib

if __name__ == '__main__':
    files = pathlib.Path('C:\\Users\\mi161303\\Desktop\\data\\_34\\').glob("20*.txt")
    for file in files:
        f = open(file, 'r', encoding='UTF-8')
        print(f.readlines()[0].split(',')[0], end=",")