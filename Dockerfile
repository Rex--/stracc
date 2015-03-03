FROM debian

RUN apt-get update && apt-get -y install python-pip
RUN pip install flask tornado dataset

RUN mkdir /stracc
ADD stracc.py /stracc
RUN mkdir -pv /stracc/db/

EXPOSE 3160

CMD ["python", "/stracc/stracc.py"]
