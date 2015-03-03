FROM debian:stable

CMD ["apt-get", "update"]
RUN apt-get -y install pip

RUN pip install flask tornado dataset

ADD stracc.py /stracc/
RUN mkdir /stracc/db

EXPOSE 3160

CMD ["python", "/stracc/stracc.py"]
