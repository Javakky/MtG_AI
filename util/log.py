import codecs
import os
from datetime import datetime


def write(name, message, dir=""):
    os.chdir('../log')
    dir = os.getcwd() + "/" + dir
    if not os.path.isdir(dir):
        os.makedirs(dir)
    path = dir + name + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".txt"
    f = codecs.open(path, 'w', 'utf_8')
    f.write(message)
    f.close()
