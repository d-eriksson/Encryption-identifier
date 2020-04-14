from os import path
class HiddenConfig:
    def __init__(self, iniPath):
        self.settings_path = iniPath
        if(not path.exists(self.settings_path)):
            f = open(self.settings_path, 'w+')
    def set_parameter(self, field, value):
        dictionary = {}
        f = open(self.settings_path, 'r')
        for line in f:
            pair = line.split(" = ")
            dictionary[pair[0]] = pair[1]
        dictionary[field] = value
        file = open(self.settings_path, "w+")
        for key, value in dictionary.items():
            file.write(str(key)+' = '+str(value)+"\n")
        return value.rstrip("\n")
    def get_parameter(self, field):
        f = open(self.settings_path, 'r')
        for line in f:
            pair = line.split(" = ")
            if pair[0] == field:
                return pair[1].rstrip("\n")
        return False
    def remove_parameter(self, field):
        dictionary = {}
        f = open(self.settings_path, 'r')
        for line in f:
            pair = line.split(" = ")
            dictionary[pair[0]] = pair[1]
        value = dictionary[field]
        del dictionary[field]
        file = open(self.settings_path, "w+")
        for key, value in dictionary.items():
            file.write(str(key)+' = '+str(value)+"\n")
        return value.rstrip("\n")

            