import os
import shutil

def open_clobber(filename):
    try:
        print(('replacing file: '+filename))
        os.remove(filename)
    except:
        print(('creating new file: '+filename))
    file_out = open(filename, 'w')
    return file_out

def clobber(filename):
    try:
        print(('replacing file: '+filename))
        os.remove(filename)
    except:
        print(('file does not exist: '+filename))
    
def copy_clobber(filename1, filename2):
    try:
        os.remove(filename2)
        print(('replacing file: '+filename2))
    except:
        print(('file does not yet exist: '+filename2))
    shutil.copyfile(filename1, filename2)



