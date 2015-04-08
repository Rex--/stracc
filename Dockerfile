FROM debian

RUN apt-get update && apt-get -y install python-pip
RUN pip install flask tornado

RUN mkdir -pv /src/stracc
ADD . /src/stracc

EXPOSE 3160

WORKDIR /src/stracc

CMD ["python", "stracc.py"]
