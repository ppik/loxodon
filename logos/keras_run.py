import keras
from keras.models import model_from_json

import numpy as np, h5py
import os
import json

import shutil
from subprocess import call
from PIL import Image
from keras.preprocessing import image
import tensorflow as tf
from time import sleep

img_generator = image.ImageDataGenerator()

with open('models/carnet-2017-11-11T14:57:39.955932-classes.json') as data_file:
    _classes_json = json.load(data_file)
    classes_json = {str(v): k for k, v in _classes_json.items()}


# load json and create mode
json_file = open('models/carnet-2017-11-11T14:57:39.955932-model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

graph = tf.get_default_graph()

# load weights into new model
loaded_model.load_weights("models/carnet-2017-11-11T14:57:39.955932-weights.h5")

# Sliding window
def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def crop_center(img,cropx,cropy):
    y,x,_ = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)
    return img[starty:starty+cropy,startx:startx+cropx, :]

def biggest_crop_center(img, cropx, cropy):
    pass
    #TODO

# returns prediction
def get_prediction(video_name):
    global graph

    predictions = []
    pop_predictions = []

    # Make sure video is saved first
    sleep(1)

    # Hackathon way to check if its an image
    if str(video_name)[-3:] == 'png' or str(video_name)[-3:] == 'jpg':
        with graph.as_default():
            #img = Image.open('videos/' + str(video_name))
            img = Image.open(str(video_name))
            np_img = crop_center(np.array(img), 299, 299)
            # winW = 150
            # winH = 300
            # for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
            prediction = loaded_model.predict(np_img.reshape(-1, np_img.shape[0], np_img.shape[1], 3))
            predictions.append(prediction)
    else:
        # Hackathon way to get hacked
        call(["ffmpeg", "-i", str(video_name), "videos/frames/out-%03d.jpg"])

        for idx, frame in enumerate(list(os.listdir('videos/frames'))):
            # Every x frames
            if idx % 15 == 0:
                img = Image.open('videos/frames/' + frame)
                np_img = crop_center(np.array(img), 299, 299)

                #np_img = np.array(img)
                with graph.as_default():
                    prediction = loaded_model.predict(np_img.reshape(-1, np_img.shape[0], np_img.shape[1], 3))
                    predictions.append(prediction)

    # Delete all files in frames folder, but leave the frames folder
    for the_file in os.listdir('videos/frames'):
        file_path = os.path.join('videos/frames', the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    # Get highest confidence value out of any predictions vector
    high_values = [0, 0, 0]
    high_class_names = ['Unknown', 'Unknown', 'Unknown']

    # Sum all probabilities for frames together
    # p = [sum(i) for i in zip(*predictions)]
    # high_values = [np.amax(p) for x in range(3)]
    # high_class_names = [np.argmax(p) for x in range(3)]

    for preds in predictions:
        index = np.argmax(preds)
        value = np.amax(preds)
        for idx, val in enumerate(high_values):
            class_name = classes_json[str(index)]
            if value > val and class_name not in high_class_names:
                high_values.insert(idx, value)
                high_class_names.insert(idx, classes_json[str(index)])
                high_values = high_values[:3]
                high_class_names = high_class_names[:3]

    # Return class_name, confidence
    return high_values[:3], high_class_names[:3]
