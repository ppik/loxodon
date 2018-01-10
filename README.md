# Social Impact Data Hack 2017 -- Loxodon challenge

This code was hacked together during [Social Impact Data Hackaton 2017](http://sidh2017.ut.ee/)
as part of Loxodon challenge within 48 hours.

See also [this blog post](http://sidh2017.ut.ee/2017/11/12/mentors-hack-teach-your-computer-to-recognize-cars/).

## Cloning

This repository uses (Git Large File Storage)[https://git-lfs.github.com/]
for storing trained models.
Ensure that the git lfs extension is installed before cloning.


## Training data

Cars Dataset http://ai.stanford.edu/~jkrause/cars/car_dataset.html

Dataset http://imagenet.stanford.edu/internal/car196/car_ims.tgz
Labels http://imagenet.stanford.edu/internal/car196/cars_annos.mat


Other possible sources:

* scraping Google image search

* scraping car sales portals (mobile.de, autoscout24.com, auto24.ee,
marktplaats.nl etc)

## Dependencies

This project uses [pipfile](https://github.com/pypa/pipfile) to manage its
Python dependencies.

Additionally it requeres that ffmpeg would be installed.

## Running the web server

Simple UI with file upload with Django
To run Django you need Python (3) and Django (latest) downloaded.
When on command line:

$ python manage.py migrate

$ python manage.py runserver

Open web-browser: http://127.0.0.1:8000/
