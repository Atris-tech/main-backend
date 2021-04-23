FROM jainal09/nemo:latest
RUN pip install gunicorn python-jose
COPY main.py .
CMD gunicorn -w 2 -b 0.0.0.0:7000 -k uvicorn.workers.UvicornWorker main:app --timeout 240