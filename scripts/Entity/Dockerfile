FROM tensorflow/tensorflow:devel-gpu
RUN apt-get update -y
RUN pip install spacy[cuda110] python-jose gunicorn fastapi[all]
RUN python -m spacy download en_core_web_lg
COPY main.py .
CMD gunicorn -w 1 -b 0.0.0.0:8006 -k uvicorn.workers.UvicornWorker main:app --timeout 120