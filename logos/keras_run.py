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

img_generator = image.ImageDataGenerator()

with open('models/carnet-2017-11-11T14:57:39.955932-classes.json') as data_file:
    classes_json = json.load(data_file)


# load json and create model
json_file = open('models/carnet-2017-11-11T14:57:39.955932-model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
graph = tf.get_default_graph()

# load weights into new model
loaded_model.load_weights("models/carnet-2017-11-11T14:57:39.955932-weights.h5")

# returns prediction
def get_prediction(video_name):
    global graph


    predictions = []

    # Hackathon way to check if its an image
    if str(video_name)[-3:] == 'png' or str(video_name)[-3:] == 'jpg':
        with graph.as_default():
            img = Image.open('videos/' + str(video_name))

            np_img = np.array(img)
            with graph.as_default():
                prediction = loaded_model.predict(np_img.reshape(-1, np_img.shape[0], np_img.shape[1], 3))
                predictions.append(prediction)
    else:

        call(["ffmpeg -i videos/" + str(video_name) + " -vf scale=299:299 videos/frames/out-%03d.jpg"], shell=True)

        for idx, frame in enumerate(list(os.listdir('videos/frames'))):
            # Every 4 frames
            if idx % 4 == 0:
                img = Image.open('videos/frames/' + frame)

                np_img = np.array(img)
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
    highest_value = -1
    highest_index = -1
    for preds in predictions:
        index = np.argmax(preds)
        value = np.amax(preds)
        if value > highest_value:
            highest_value = value
            highest_index = index


    # Get brand name of the highest confidence value prediction
    brand_name = 'Unknown'
    for brand, idx in classes_json.items():
        if idx == highest_index:
            brand_name = brand
            break

    # Return class_name, confidence
    return brand_name, highest_value
