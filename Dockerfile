FROM debian

RUN apt-get update && apt-get -y install python-pip
RUN pip install flask tornado dataset

RUN mkdir -pv /src/stracc
ADD stracc.py /src/stracc/stracc.py
RUN mkdir -pv /src/stracc/db/

EXPOSE 3160

CMD ["python", "/stracc/stracc.py"]
