import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import time

from fileHandler import (extract_data_from_all_files,
                        read_data_from_file,
                        divide_test_and_trainging_data,
                        data_from_file,
                        get_all_files_in_dir,
                        create_map,
                        map_to_file,
                        stringToInt)
from encrypter import (encrypt_file, decrypt_file, encrypt_file_header_skip)



def prepare_data():
    divide_test_and_trainging_data("OriginalFiles", "Test", "Training")
    print("Files divided")
    #Training Data
    files = get_all_files_in_dir("Training")
    file_map = create_map(files)
    map_to_file(file_map, "Training" + "_map")
    print("Training map done")
    for file_path, value in file_map.items():
        if(value == 1):
            encrypt_file(file_path)
    print("Training data encrypted")
    extract_data_from_all_files("Training_data.txt", file_map )
    print("Training data extracted")
    #Test Data
    files = get_all_files_in_dir("Test")
    file_map = create_map(files)
    map_to_file(file_map, "Test_map")
    print("Test map done")
    for file_path, value in file_map.items():
        if(value == 1):
            encrypt_file(file_path)
    print("Test data encrypted")
    extract_data_from_all_files("Test_data.txt", file_map )
    print("Test data extracted")

def train_model(layers,activationLayers,opti,lss):

    model = keras.Sequential()
    model.add(keras.layers.Dense(layers[0], activation=activationLayers[0], input_dim=10))
    for l in range(1, len(layers)):
        model.add(keras.layers.Dense(layers[l], activation = activationLayers[l]))

    model.compile(optimizer=opti, loss=lss)

    trainingDataInput, trainingDataOutput = read_data_from_file("Training_data.txt")
    #for data in trainingDataInput:
    #    print(data)
    #    print("\n")
    trainingInputTensor = tf.constant(trainingDataInput)
    trainingOutputTensor = tf.constant(trainingDataOutput)
    model.fit(trainingInputTensor,trainingOutputTensor, batch_size=len(trainingDataInput), epochs=2000, shuffle=True)
    keras.utils.plot_model(
        model,
        to_file='model.png',
        show_shapes=True,
        show_layer_names=True,
        rankdir='LR',
        expand_nested=True,
        dpi=96
    )
    testDataInput, testDataOutput = read_data_from_file("Test_data.txt")
    testInputTensor = tf.constant(testDataInput)
    eval = model.predict(testInputTensor, batch_size=len(testDataInput))
    save_results(layers, activationLayers, opti, lss, eval, testDataOutput, len(trainingDataInput))
    #print(model.get_layer(index=0).weights)
    #model.save('./models/latest', True)
    return model
def load_latest_model():
    model = keras.models.load_model('./models/latest')
    return model
def is_encrypted(filepath, model):
    data = []
    temp_data = data_from_file(filepath)
    temp_data[0]= float(stringToInt(temp_data[0]))
    temp_data = [float(i) for i in temp_data]
    data.append(temp_data)
    
    InputTensor = tf.constant(data)
    prediction = model.predict(InputTensor)[0][0]
    return prediction
def save_results(layers, activationLayers, optimizer, loss, evaluation, testDataAnswers, num_training_data):
    f= open("results.txt","a+")
    id = get_last_id()
    f.write("************************************\n")
    f.write (time.asctime( time.localtime(time.time()) ))
    f.write("\n")
    f.write("id: %s \n" % str(id))
    f.write("Files in training data: %s\n" % num_training_data)
    f.write("Files in test data: %s\n" % len(testDataAnswers))
    f.write("Optimizer: %s \n" % optimizer)
    f.write("Loss: %s \n" % loss)
    f.write("Number of layers: %s \n" % len(layers))
    for i in range(0,len(layers)):
        f.write("%s_%s \n" % (layers[i], activationLayers[i]))
    highest_diff = 0.0
    average_diff = 0.0
    ninety_fifth_percentile = 0
    i=0
    for e in evaluation:
        #print(round(e[0],6) , " -> " , testDataAnswers[i][0])
        if highest_diff < abs(round(e[0],16)-testDataAnswers[i][0]):
            highest_diff = abs(round(e[0],16)-testDataAnswers[i][0])
        average_diff += abs(round(e[0],16)-testDataAnswers[i][0])
        if (testDataAnswers[i][0] < 0.5 and  round(e[0],6) < 0.05):
            ninety_fifth_percentile += 1
        elif (testDataAnswers[i][0] > 0.5 and  round(e[0],6) > 0.95):
            ninety_fifth_percentile += 1
        i+=1
    average_diff /= i
    ninety_fifth_percentile /=i
    f.write("Highest diff: %s\n" % highest_diff)
    f.write("Average diff: %s\n" % average_diff)
    f.write("95 percent certainty: %s\n" % ninety_fifth_percentile)
    f.write("************************************\n")
    f.close()
    f = open("trunc_results.txt","a+")
    f.write(str(id))
    f.write('$')
    f.write(time.asctime( time.localtime(time.time())))
    f.write('$')
    f.write(str(num_training_data))
    f.write('$')
    f.write(str(len(testDataAnswers)))
    f.write('$')
    f.write(str(optimizer))
    f.write('$')
    f.write(str(loss))
    f.write('$')
    f.write(str(len(layers)))
    f.write('$')
    f.write(str(highest_diff))
    f.write('$')
    f.write(str(average_diff))
    f.write('$')
    f.write(str(ninety_fifth_percentile))
    f.write('\n')
    f.close()
def read_results(lines):
    f=open('trunc_results.txt', 'r')
    data = []
    idx = 0
    for line in f:
        if(idx >= lines[0] and idx <= lines[1] ):
            line_data = {}
            temp = line.split('$')
            line_data["id"] = temp[0]
            line_data["date"] = temp[1]
            line_data["num_training_data"] = temp[2]
            line_data["num_test_data"] = temp[3]
            line_data["optimizer"] = temp[4]
            line_data["loss"] = temp[5]
            line_data["num_layers"] = temp[6]
            line_data["highest_diff"] = temp[7]
            line_data["average_diff"] = temp[8]
            line_data["amount_over_ninety_five"] = temp[9]
            data.append(line_data)
        idx+=1
    return(data)
    f.close()
def get_last_id():
    f=open('trunc_results.txt', 'r')
    id = 0
    for line in f:
        id += 1
    return id
def flatten_results(input, output, data):
    i = []
    o = []
    for d in data:
        i.append(d[input])
        o.append(float(d[output]))
    return(i,o)

def print_fig(names ,figname, lines): 
    res =read_results(lines)
    fig, ax = plt.subplots()
    for name in names:
        input, output = flatten_results("id",name,res)
        ax.plot(input, output, label=name)
    ax.legend()

    plt.savefig(figname+".png", dpi=512)

#prepare_data()

activationLayers = ["hard_sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid","sigmoid"]
opti = 'RMSprop' # Best Performance
lss = tf.keras.losses.BinaryCrossentropy() # Best Performance
layers = [64,8,8,1]
model = train_model(layers,activationLayers,opti,lss)

#model = load_latest_model()
#model2.summary()
#model.summary()
#print_fig(["average_diff", "highest_diff"], "figure", [0,59])