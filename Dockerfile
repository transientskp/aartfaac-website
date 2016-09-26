FROM kernsuite/base:1


RUN docker-apt-install python-casacore

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /code
WORKDIR /code
