FROM huggingface/transformers-pytorch-gpu
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt-get update -y
RUN pip install neuralcoref bert-extractive-summarizer git+https://github.com/LIAAD/yake python-jose gunicorn fastapi[all]
COPY main.py .
CMD gunicorn -w 1 -b 0.0.0.0:8005 -k uvicorn.workers.UvicornWorker main:app --timeout 120
