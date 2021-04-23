FROM python:3.7-buster
RUN apt-get update -y
RUN wget http://ftp.br.debian.org/debian/pool/main/o/openjdk-8/openjdk-8-jre-headless_8u252-b09-1~deb9u1_amd64.deb
RUN wget http://ftp.br.debian.org/debian/pool/main/o/openjdk-8/openjdk-8-jdk-headless_8u252-b09-1~deb9u1_amd64.deb
RUN apt install -y ./openjdk-8-jre-headless_8u252-b09-1~deb9u1_amd64.deb
RUN apt install -y ./openjdk-8-jdk-headless_8u252-b09-1~deb9u1_amd64.deb
RUN pip install nlu pyspark==2.4.7 python-jose gunicorn fastapi[all]
COPY download.py .
RUN python download.py
COPY . .
CMD gunicorn -w 2 -b 0.0.0.0:8007 -k uvicorn.workers.UvicornWorker main:app --timeout 120