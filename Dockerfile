FROM debian:stable

RUN apt-get update && apt-get install pip

RUN pip install flask tornado dataset

ADD stracc.py /stracc/
RUN mkdir /stracc/db

EXPOSE 3160

CMD ["python", "/stracc/stracc.py"]
