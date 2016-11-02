FROM kernsuite/base:1

# note: not sure if tk is required if we choose different matplotlib backend
RUN docker-apt-install python3-casacore python3-pip python3-tk ffmpeg

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN mkdir /code
WORKDIR /code
