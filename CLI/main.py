import argparse
import tensorflow as tf
from ML import (prepare_data,
                train_model,
                load_latest_model,
                is_encrypted,
                print_fig)

def prepare(args):
    prepare_data()

def encrypt(args):
    print("encrypt")

def decrypt(args):
    print("decrypt")

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
    model = train_model(layers,activationLayers,opti,lss)

def test(args):
    model = load_latest_model()
    enc = is_encrypted(args.file, model)
    print(str(round(enc,3)) + "% chance of encryption")

def main():

    parser = argparse.ArgumentParser()
    FUNCTION_MAP = {'train' : train,
                    'test' : test,
                    'prepare' : prepare,
                    'encrypt' : encrypt,
                    'decrypt' : decrypt }
    parser.add_argument('command', choices=FUNCTION_MAP.keys())

    parser.add_argument('--file',action="store", dest="file")
    parser.add_argument('--add',action="append", dest="layers")
    parser.add_argument('--opti',action="store", dest="opti", default="RMSprop")
    parser.add_argument('--lss',action="store", dest="lss", default="binary_crossentropy")
    
    args = parser.parse_args()
    func = FUNCTION_MAP[args.command]
    func(args)
if __name__ == "__main__":
    main()