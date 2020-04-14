from sftpserver import start_server
HOST, PORT = 'localhost', 3373
def main():
    start_server(HOST, PORT, './key/backup.key', 'DEBUG')
if __name__ == '__main__':
    main()