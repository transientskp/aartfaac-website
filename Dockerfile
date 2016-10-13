FROM kernsuite/base:1

RUN docker-apt-install python3-casacore python3-pip

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN mkdir /code
WORKDIR /code
