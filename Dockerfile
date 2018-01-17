FROM python:3.6-slim

# -- Create Application directory:
RUN mkdir /app
WORKDIR  /app

# -- Adding Pipfiles
COPY Pipfile* /app/

# -- Install dependencies:
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system && \
    echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y -t jessie-backports install ffmpeg

RUN apt install -y wget 
# as make was not working...
#RUN apt install -y build-essential

COPY . /app

RUN cd darknet
#RUN make
RUN wget https://pjreddie.com/media/files/tiny-yolo.weights
RUN cd ..

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
