from fileHandler import data_from_file
from fileHandler import get_all_files_in_dir
from fileHandler import backup
from fileHandler import extract_data_from_all_files
from fileHandler import read_data_from_file
from fileMapper import create_map
from fileMapper import map_to_file
from fileMapper import file_to_map
from encrypter import encrypt_file
from encrypter import decrypt_file
import sys

def menu():
    print("************MAIN MENU**************")
    print()
    choice = input("""
    A: Backup system
    B: Create file map for /Files
    C: Create file map for /Test
    D: Encrypt files
    E: Decrypt files
    F: Reset system
    G: Extract all data from /Files
    H: Extract all data from /Test
    Q: Quit/Log Out

    Please enter your choice: """)

    if choice == "A" or choice =="a":
        backup_system()
    elif choice == "B" or choice =="b":
        create_file_map("Files")
    elif choice == "C" or choice =="c":
        create_file_map("Test")
    elif choice=="D" or choice=="d":
        encrypt_files()
    elif choice=="E" or choice=="e":
        decrypt_files()
    elif choice=="F" or choice=="f":
        reset()
    elif choice=="G" or choice=="g":
        extract_all_data("Files")
    elif choice=="H" or choice=="h":
        extract_all_data("Test")
    elif choice=="Q" or choice=="q":
        sys.exit()
    else:
        print("You must only select either A, B, C, D, E or Q.")
        print("Please try again")
    menu()
def reset():
    backup("OriginalFiles", "Files")
    file = open("data.txt", "w")
    file.close()
    file = open("Files_map.txt", "w")
    file.close()
def backup_system():
    backup("Files", "Backup")
def create_file_map(dirName):
    files = get_all_files_in_dir(dirName)
    file_map = create_map(files)
    map_to_file(file_map, dirName + "_map")
    return file_map
def encrypt_files():
    encryption_key = b'SZtDJqmum3GXH2pxaWKqUP4Ai0VLb2jXq4pv3IFFB2c='
    map = file_to_map("Test_map.txt")
    for file_path, value in map.items():
        if(value == 1):
            encrypt_file(file_path,encryption_key)
def decrypt_files():
    encryption_key = b'SZtDJqmum3GXH2pxaWKqUP4Ai0VLb2jXq4pv3IFFB2c='
    map = file_to_map("Files_map.txt")
    for file_path, value in map.items():
        if(value == 1):
            decrypt_file(file_path,encryption_key)
def extract_all_data(dirName):
    extract_data_from_all_files(dirName+"_data.txt", file_to_map(dirName+"_map.txt") )
    data = read_data_from_file(dirName+"_data.txt")
    
menu()