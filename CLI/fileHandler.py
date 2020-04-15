from os import (walk,path,mkdir, listdir,unlink)
from shutil import (copy,rmtree)
import binascii
from entropy import calculate_entropy
from random import random

def create_map(fileList):
    map = {}
    for file in fileList:
        map[file] = int(random()>0.5)
    
    return map

def map_to_file(map, mapname):
    file = open(mapname + ".txt", "w+")
    for key, value in map.items():
        file.write(key+'$'+str(value)+"\n")
    file.close()

def file_to_map(fileName):
    if not path.exists(fileName):
        file = open(fileName, "w+")
        file.close()

    file = open(fileName, "r")
    map = {}
    for line in file:
        data = line.split('$',1)
        map[data[0]] = int(data[1])
    file.close()
    return map
def append_to_file(fileName, s):
    id = 0
    file = open(fileName, "r")
    for line in file:
        id += 1
    file.close()
    file = open(fileName, "a+")
    file.write(s+'$'+str(id)+'\n')
    return id
def delete_all_files_in_dir(folder):
    for filename in listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
def data_from_file(path):
    file = open(path, "br")
    data = []
    data.append(path.split('.')[-1])
    data.append(calculate_entropy(path))
    for i in range(0,8):
        data.append(int.from_bytes(file.read(1), byteorder='little'))
    file.close()
    return data

def get_all_files_in_dir(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            f.append(dirpath + "/" + file)
    return f
def extract_data_from_all_files(writepath, map):
    file = open(writepath, "w")
    for key, value in map.items():
        data = data_from_file(key)
        file.write(str(value))
        for d in data:
            if(type(d) == str):
                file.write('$'+d)
            else:
                file.write('$'+str(d))
        file.write("\n")
    file.close()
def read_data_from_file(path):
    file = open(path, "r")
    data = []
    answers = []
    for line in file:
        temp_data = line.split('$')
        temp_data[-1] = temp_data[-1].split('\n')[0]

        temp_answers = []
        temp_answers.append(float(temp_data.pop(0)))
        answers.append(temp_answers)

        temp_data[0]= float(stringToInt(temp_data[0]))
        temp_data = [float(i) for i in temp_data]
        data.append(temp_data)
    file.close()
    return data,answers
def backup(originalPath, backupPath):
    for (dirpath, dirnames, filenames) in walk(originalPath):
        for file in filenames:
            pathName =  dirpath +'/' + file
            directory = dirpath +'/'

            newPathName = directory.strip(originalPath)
            newPathName = backupPath + newPathName
            if not path.exists(newPathName):
                mkdir(newPathName)
            copy(pathName, newPathName)


def divide_test_and_trainging_data(originalPath, testPath, trainingPath):
    delete_all_files_in_dir(testPath)
    delete_all_files_in_dir(trainingPath)
    for (dirpath, dirnames, filenames) in walk(originalPath):
        for file in filenames:
            pathName =  dirpath +'/' + file
            directory = dirpath +'/'

            newPathName = directory.strip(originalPath)
            backupPath = trainingPath
            if random() < 0.1:
                backupPath = testPath
            newPathName = backupPath + newPathName
            if not path.exists(newPathName):
                mkdir(newPathName)
            copy(pathName, newPathName)
file_types = {}
file_types = file_to_map("file_types.txt")
def stringToInt(s):
    if not s in file_types:
        file_types[s] = append_to_file("file_types.txt", s)
    return file_types[s]
