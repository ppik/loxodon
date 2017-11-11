# Social Ipact Data Hack 2017 -- Loxodon challenge

## Training data

Cars Dataset http://ai.stanford.edu/~jkrause/cars/car_dataset.html

Dataset http://imagenet.stanford.edu/internal/car196/car_ims.tgz
Labels http://imagenet.stanford.edu/internal/car196/cars_annos.mat


Other possible sources:

* scraping Google image search

* scraping car sales portals (mobile.de, autoscout24.com, auto24.ee, marktplaats.nl etc)


## Running the web server

Simple UI with file upload with Django
To run Django you need Python (3) and Django (latest) downloaded.
When on command line:

$ git clone https://github.com/varje/loxodon.git
$ python manage.py migrate
$ python manage.py runserver

Open web-browser: localhost:8000/logos/ or http://127.0.0.1:8000/logos/
