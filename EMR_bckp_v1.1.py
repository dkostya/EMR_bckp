import os
from ftplib import FTP
import datetime

emrlist = open('emrlist.txt', 'r')
settings = open('settings.txt', 'r')
hostdir = settings.readlines()[1]

print('EMR BACKUP v.1.1. Для продолжения нажмите Enter')
input()

for line in emrlist:
    timeshtamp = ((str(datetime.datetime.now()))[:-7]).replace(':', '-')
    os.chdir(hostdir)
    os.makedirs(line.rstrip('\n'), exist_ok=True)
    os.chdir(line.rstrip('\n'))
    endIP = (line.rstrip('\n'))[((line.rstrip('\n'))).rfind('.'):]
    timeshtamp += ' ' + 'IP' + endIP
    os.mkdir(timeshtamp)
    os.chdir(timeshtamp)
    print('Соединение с EMR', line)
    try:
        ftp = FTP(line.rstrip('\n'), 'target', 'target')
        ftp.cwd('/tffs0/para/')
        files = ftp.nlst()
        print('Копирование параметров EMR', line)
        files = filter(lambda x: x.endswith('gz'), files)
        for file in files:
            ftp.retrbinary('RETR '+file, open(os.path.join(os.curdir, file), 'wb').write, 1024)
            print(file, 'done')
        ftp.close()
    except:
        print('Ошибка соединения с EMR', line)
    print()

emrlist.close()
settings.close()

print('Копирование завершено. Для выхода нажмите Enter')
input()
