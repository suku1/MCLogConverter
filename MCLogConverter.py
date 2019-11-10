import os
import gzip
import re
import shutil

ptrs = []

def add_patterns():
    ptrs.append(re.compile('^\[[0-2][0-9]:[0-9][0-9]:[0-9][0-9]\] \[Client thread/ERROR\]: '))
    ptrs.append(re.compile('^\[[0-2][0-9]:[0-9][0-9]:[0-9][0-9]\] \[Client thread/WARN\]: '))

def matching(txt):
    for ptr in ptrs:
        if re.search(ptr, txt):
            return True
    return False

def read_file(fpath):
    if re.search('\.log.gz$', fpath, re.IGNORECASE):
        return gzip.open(fpath, 'rt', encoding='cp932', errors='ignore'), 'gzip'
    elif re.search('\.log$', fpath, re.IGNORECASE):
        return open(fpath, 'r', encoding='cp932', errors='ignore'), 'log'
    else:
        return False, ''

def conv(root, fname, backup=''):
    if backup == '': backup = os.path.join(root, 'backup')
    if os.path.isdir(backup) == False:
        if os.path.isfile(backup): 
            print('Error!')
            return
        os.makedirs(backup)

    fpath = os.path.join(root, fname)
    bpath = os.path.join(backup, fname)
    fsize = os.path.getsize(fpath) // 1024

    f, ex = read_file(fpath)
    if f == False: 
        print(fpath + ' is not log file.\n')
        return

    print('filename: ' + fpath)
    print('filesize: ' + str(fsize) + ' KB')
    shutil.copy2(fpath, bpath)
    print('backup path: ' + bpath)

    new_data = ''

    try:
        line = f.readline()
    except:
        print(fpath + ' is not log file.\n')
        return

    while line:
        if matching(line) == False: new_data += line
        line = f.readline()
    f.close()

    if ex == 'log':
        with open(fpath, 'w', encoding='cp932') as f:
            f.write(new_data)
    elif ex == 'gzip': 
        with gzip.open(fpath, 'wt', encoding='cp932') as f:
            f.write(new_data)
    print('complete.\n')

def main():
    root = 'C:/Users/User/AppData/Roaming/.minecraft/logs'
    add_patterns()
    ls = os.listdir(root)
    length = str(len(ls))
    for i, name in enumerate(ls):
        print(str(i+1) + '/' + length + ' files')
        conv(root, name)

if __name__ == '__main__':
    main()
