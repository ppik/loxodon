#!/usr/bin/env python

import os
from os.path import basename, exists
from glob import glob
from random import seed, sample
from math import ceil

from scipy.io import loadmat

DATA_PATH = 'data/'
VALID_RATIO = 0.2

seed(20171111)

info = loadmat(DATA_PATH + 'cars_annos.mat')

class_names = []
for name in info['class_names'].squeeze():
    parts = name[0].lower().split()

    class_name = parts[0]

    if parts[1] in {'general', 'karma', 'martin', 'rover'}:
        class_name += '_' + parts[1]

    class_names.append(class_name)

# 49 diffreent classes


## Create training set

for item in info['annotations'].squeeze():
    image = DATA_PATH + item[0][0]
    make = class_names[item[5][0][0] - 1] # Matlab uses 1-based indexing

    dest = DATA_PATH + 'train/' + make + '/' + basename(image)

    if exists(image):
        os.renames(image, dest)

## Create validation set

makes = glob(DATA_PATH + 'train/*')

for make in makes:
    images = glob(make + '/*')

    data_size = len(images)
    validation_size = ceil(data_size*VALID_RATIO)

    for image in sample(images, validation_size):
        os.renames(image, image.replace('train/', 'valid/', 1))
