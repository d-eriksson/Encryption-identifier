from cryptography.fernet import Fernet
from fileHandler import data_from_file

def encrypt_file(filename, key=None):
    file = open(filename, 'br')
    if key == None:
        key = Fernet.generate_key()
        f = Fernet(key)
    else:
        f = Fernet(key)
    lines = []
    newline = b'\n'
    for line in file:
        lines.append(f.encrypt(line)+newline)
    file.close()
    file = open(filename, 'bw')
    file.writelines(lines)
    file.close()
    return key
def encrypt_file_header_skip(filename, key=None):
    file = open(filename , 'br')
    if key == None:
        key = Fernet.generate_key()
        f = Fernet(key)
    else:
        f = Fernet(key)
    lines = []
    newline = b'\n'
    firstLine = True
    for line in file:
        if firstLine:
            lines.append(line)
            firstLine = False
        else:
            lines.append(f.encrypt(line)+newline)
    file.close()
    file = open(filename,'bw')
    file.writelines(lines)
    file.close()
    return key
def decrypt_file(filename, key):
    file = open(filename, 'br')
    lines = []
    f = Fernet(key)
    for line in file:
        lines.append(f.decrypt(line))
    file.close()
    file = open(filename, 'bw')
    file.writelines(lines)
    file.close()

#encrypt_file_header_skip("figure.png")
#data = data_from_file("model.png")
#print(data)