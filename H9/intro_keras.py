'''
Created on Nov 18, 2020

@author: Jason Chen
'''

import tensorflow as tf
from tensorflow import keras


def get_dataset(training=True):
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    if training == True:
        return (train_images, train_labels)
    else:
        return (test_images, test_labels)
    
def print_stats(train_images, train_labels):
    totalNumImg, imgDimenX, imgDimenY = train_images.shape
    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    six = 0
    seven = 0
    eight = 0
    nine = 0
    
    for x in train_labels:
        if x == 0:
            zero += 1
        if x == 1:
            one += 1
        if x == 2:
            two += 1
        if x == 3:
            three += 1
        if x == 4:
            four += 1
        if x == 5:
            five += 1
        if x == 6:
            six += 1
        if x == 7:
            seven += 1
        if x == 8:
            eight += 1
        if x == 9:
            nine += 1
            
    print(totalNumImg)
    print(str(imgDimenX) + 'x' + str(imgDimenY))
    print('0. Zero - ' + str(zero))
    print('1. One - ' + str(one))
    print('2. Two - ' + str(two))
    print('3. Three - ' + str(three))
    print('4. Four - ' + str(four))
    print('5. Five - ' + str(five))
    print('6. Six - ' + str(six))
    print('7. Seven - ' + str(seven))
    print('8. Eight - ' + str(eight))
    print('9. Nine - ' + str(nine))
    

def build_model():
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape = (image_shape())))
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dense(10))
    opt = keras.optimizers.SGD(learning_rate=0.001)
    loss1 = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    metric1 = keras.metrics.Accuracy()
    model.compile(optimizer=opt, loss=loss1, metrics=['accuracy'])
    
    return model
            
     
def train_model(model, train_images, train_labels, T):
    model.fit(train_images, train_labels, epochs=T)       
            
            
def evaluate_model(model, test_images, test_labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
    accuracyPercent = test_accuracy * 100
    accuracy = '{:.2f}'.format(accuracyPercent)
    loss = '{:.4f}'.format(test_loss)
    if show_loss == True:
        print('Loss: ' + loss)
        print('Accuracy: ' + accuracy + '%')
    else:
        print('Accuracy: ' + accuracy + '%')


def predict_label(model, test_images, index):
    predResults = model.predict(test_images)
    numMaxIndex = None
    numMax = None
    maxList = []
    for x in range(len(predResults[index])):
        numLabel = None
        if x == 0:
            numLabel = 'Zero'
        if x == 1:
            numLabel = 'One'
        if x == 2:
            numLabel = 'Two'
        if x == 3:
            numLabel = 'Three'
        if x == 4:
            numLabel = 'Four'
        if x == 5:
            numLabel = 'Five'
        if x == 6:
            numLabel = 'Six'
        if x == 7:
            numLabel = 'Seven'
        if x == 8:
            numLabel = 'Eight'
        if x == 9:
            numLabel = 'Nine'
            
        elem = {'labelNum': numLabel, 'prob': predResults[index][x]}
        maxList.append(elem)
            
    maxListSorted = sorted(maxList, key=lambda i : (i["prob"]), reverse=True)
    
    for iteNum in range(3):
        numProb = '{:.2f}'.format(maxListSorted[iteNum]['prob']*100)
        print(maxListSorted[iteNum]['labelNum'] + ': ' + numProb + '%')
        


            
            
def image_shape():
    (train_images, train_labels) = get_dataset() 
    totalNumImg, imgDimenX, imgDimenY = train_images.shape
    return imgDimenX, imgDimenY
            
            
def add_softmax(model):
    model.add(keras.layers.Softmax())
            
            
            
            
            
            
            