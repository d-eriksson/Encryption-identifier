import paramiko
from stat import S_ISDIR, S_ISREG
from os import (walk, path, mkdir)
def removeAfterLastOccurance(string, char):
    string2 = ''
    length = len(string)
    i = 0

    while(i < length):
        if(string[i] == char):
            string2 = string[0 : i+1]
        i = i + 1
    return string2
def create_all_dir(string):
    lst = string.split("/")
    lst = lst[1:-1]
    print(lst)
    for i in range(len(lst)-1,-1,-1):
        pfix ="./"
        print(lst[i])
        for k in range(0, i): 
            pfix = pfix + lst[k] + "/"
        lst[i] = pfix + lst[i]
    
    for dir in lst:
        if not path.exists(dir):
            mkdir(dir)

    print(lst)

class BackupConnector: 
    def __init__(self, key_path, local_root_path, model):
        self.model = model
        pkey = paramiko.RSAKey.from_private_key_file(key_path)
        transport = paramiko.Transport(('localhost', 3373))
        transport.connect(username='admin', password='admin', pkey=pkey)
        self.sftp = paramiko.SFTPClient.from_transport(transport)
        self.local_root_path = local_root_path
        if self.local_root_path[-1] == '/':
            self.local_root_path = self.local_root_path[:-1:]
    def printDir(self):
        print(self.sftp.listdir('.'))
    def file_exists(self, path, file):
        lst = self.sftp.listdir(path)
        return file in lst
    def backup_to_server(self):
        for (dirpath, dirnames, filenames) in walk(self.local_root_path):
            for file in filenames:
                local_path =  dirpath +'/' + file
                directory = dirpath
                server_path = dirpath.replace(self.local_root_path,"")
                server_dir = '.' + server_path + '/'
                server_path = '.' + server_path + '/' + file
                print(local_path)
                file = open(local_path, 'rb')
                self.sftp.putfo(file, server_path)
                file.close()
    def revert_from_backup(self):
        files = self.server_file_array(".")
        for entry in files:
            local_path = self.local_root_path + entry[1:]
            if path.exists(local_path):
                f = open(local_path, "wb+")
                self.sftp.getfo(entry, f)
            else:
                create_all_dir(local_path)
                f = open(local_path, "wb+")
                self.sftp.getfo(entry, f)

    def server_file_array(self, root):
        newList = []
        for entry in self.sftp.listdir_attr(root):
            mode = entry.st_mode
            if S_ISDIR(mode):
                newList.extend(self.server_file_array(root + "/" + entry.filename))
            elif S_ISREG(mode):
                newList.append(root + "/" + entry.filename)
        return newList