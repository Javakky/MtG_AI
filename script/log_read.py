import pathlib

if __name__ == '__main__':
    for i in range(1, 81):
        files = pathlib.Path('C:\\Users\\mi161303\\Desktop\\log\\' + str(i) + '\\').glob("20*.txt")
        for file in files:
            f = open(file, 'r', encoding='UTF-8')
            print(f.readlines()[1].split(',')[0].replace("\n",""), end=",")
        print()
