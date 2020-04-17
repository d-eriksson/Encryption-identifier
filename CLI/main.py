import argparse
import configparser
from os import (walk,path,mkdir, listdir,unlink)
from shutil import (copy,rmtree)
import tensorflow as tf
from ML import (prepare_data,
                train_model,
                load_latest_model,
                is_encrypted,
                print_fig)

def prepare(args):
    prepare_data()
def config(args):
    abort = False
    if not args.root:
        print("Missing --root argument")
        abort = True
    if not args.backup_path:
        print("Missing --backup_path argument")
        abort = True
    if abort:
        return
    write_config = configparser.ConfigParser()

    write_config.add_section("Paths")
    write_config.set("Paths","root",args.root)
    write_config.set("Paths","backup_path", args.backup_path)
    print(args.root)
    cfgfile = open("my.ini",'w+')
    write_config.write(cfgfile)
    cfgfile.close()
def readConfig():
    read_config = configparser.ConfigParser()
    read_config.read("my.ini")

    root = read_config.get("Paths", "root")
    backupPath = read_config.get("Paths", "backup_path")
    return root, backupPath

def backup_data(args):
    model = load_latest_model()
    for (dirpath, dirnames, filenames) in walk(args.rootPath):
        for file in filenames:
            pathName =  dirpath +'/' + file
            directory = dirpath +'/'
            enc_risk = is_encrypted(pathName,model)
            if enc_risk < 0.99:
                newPathName = directory.strip(args.rootPath)
                newPathName = args.backupPath + newPathName
                if not path.exists(newPathName):
                    mkdir(newPathName)
                #print("pathName: " + pathName + " - newPathName: " + newPathName)
                copy(pathName, newPathName)
            else:
                if args.abort:
                    print("Found encrypted file aborting backup")
                    return
                if args.restore:
                    BackupFilePath = args.backupPath + directory.strip(args.rootPath) + file
                    copy(BackupFilePath, dirpath + '/')
                #print(pathName + " is encrypted!")
def check_for_encrypted_files(args):
    model = load_latest_model()
    encryptedFiles = 0
    for(dirpath, dirnames, filenames) in walk(args.checkPath):
        for file in filenames:
            enc_risk = is_encrypted(dirpath + '/' + file, model)
            if not enc_risk < 0.99:
                encryptedFiles += 1
    
    print("There are " + str(encryptedFiles) + " encrypted files in " + args.checkPath)
def train(args):
    activationLayers = []
    layers = []
    if(args.layers):
        for layer in args.layers:
            split = layer.split('-')
            layers.append(int(split[0]))
            activationLayers.append(split[1])
    else:
        activationLayers = ["hard_sigmoid","sigmoid","sigmoid","sigmoid"]
        layers = [64,8,8,1]
    opti = args.opti
    lss = args.lss
    epochs = int(args.epochs)
    model = train_model(layers,activationLayers,opti,lss,epochs)

def test(args):
    model = load_latest_model()
    enc = is_encrypted(args.file, model)
    print(str(round(enc,3)) + "% chance of encryption")
def figure(args):
    print_fig(args.x, args.y, args.figure_name, [int(args.figure_start),int(args.figure_end)], args.figure_title)

def main():
    
    
    parser = argparse.ArgumentParser()
    FUNCTION_MAP = {'train' : train,
                    'test' : test,
                    'prepare' : prepare,
                    'backup' : backup_data,
                    'config' : config,
                    'figure': figure,
                    'check' : check_for_encrypted_files}
    parser.add_argument('command', choices=FUNCTION_MAP.keys())

    parser.add_argument('--file',action="store", dest="file", help="Path to file. [test]")

    parser.add_argument('--add',action="append", dest="layers", help="Adds a layer ([number_of_nodes]-[activation_method]). [train]")
    parser.add_argument('--opti',action="store", dest="opti", default="RMSprop", help="Set the optimizer. [train]")
    parser.add_argument('--lss',action="store", dest="lss", default="binary_crossentropy", help="Set the loss function. [train]")
    parser.add_argument('--epochs',action="store", dest="epochs", type=int, default=2000, help="Set the loss function. [train]")

    parser.add_argument('--abort',action="store_true", dest="abort", default=False,help="Aborts backup as soon one encrypted file is found. [backup]")
    parser.add_argument('--restore',action="store_true", dest="restore", default=False,help="Restores encrypted files from backup if found while backing up non-encrypted files. [backup]")

    parser.add_argument('--root', action="store", dest="root", default="Test",help="Set root path for backup. [config]" )
    parser.add_argument('--backup_path', action="store", dest="backup_path",default="Backup", help="Set backup path for backup. [config]")


    parser.add_argument('--check_path', action="store", dest="checkPath",default="BackupTest", help="Set path for checking number of encrypted files. [config]")

    parser.add_argument('--y', action="append", dest="y", default=["average_diff", "highest_diff"], help="Set fields for x in figure.. [figure]")
    parser.add_argument('--x', action="store", dest="x", default="id", help="Set field for x in figure. [figure]")
    parser.add_argument('--figure_name', action="store", dest="figure_name", default="figure", help="Set figure name. [figure]")
    parser.add_argument('--figure_start', action="store", dest="figure_start", default=0, help="Set figure start. [figure]")
    parser.add_argument('--figure_end', action="store", dest="figure_end", default=1000, help="Set figure end. [figure]")
    parser.add_argument('--figure_title', action="store", dest="figure_title", default="Figure", help="Set figure figure title. [figure]")
    
    
    args = parser.parse_args()

    args.rootPath, args.backupPath = readConfig()

    func = FUNCTION_MAP[args.command]
    func(args)
if __name__ == "__main__":
    main()