FROM debian

RUN apt-get update && apt-get -y install python-pip
RUN pip install flask tornado dataset

RUN mkdir -pv /src/stracc
ADD stracc.py /src/stracc/stracc.py

EXPOSE 3160

CMD ["python", "/src/stracc/stracc.py"]
