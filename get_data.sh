#!/usr/bin/env bash

mkdir -p data
cd data


if [ ! -a 'car_ims.tgz' ] ; then
    wget http://imagenet.stanford.edu/internal/car196/car_ims.tgz
fi

if [ ! -a 'cars_annos.mat' ] ; then
    wget http://imagenet.stanford.edu/internal/car196/cars_annos.mat
fi

tar -xzf car_ims.tgz
