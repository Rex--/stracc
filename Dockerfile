FROM debian

RUN apt-get update && apt-get -y install python-pip
RUN pip install flask tornado dataset

ADD stracc.py /stracc

EXPOSE 3160

CMD ["python", "/stracc/stracc.py"]
