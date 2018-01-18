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

COPY . /app

RUN apt install -y build-essential git wget

RUN git clone https://github.com/MadisKarli/darknet

WORKDIR darknet
RUN make
RUN bash start_me_first.sh

WORKDIR /app

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
