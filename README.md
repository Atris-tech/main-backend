# main-backend
## Micro services
```shell
docker commit `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` jainal09/nemo:latest
docker exec -it `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` bash
docker stop `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'`
```

```shell
pm2 start "docker run -p 8765:8765 lowerquality/gentle"
```

```shell
pm2 start "docker run --gpus all -p 7000:7000 jainal09/nemo:prod"
```

```shell
pm2 start "docker run -p 5000:5000 quay.io/codait/max-audio-classifier"
```

```shell
pm2 start "docker run -p 9000:5000 quay.io/codait/max-resnet-50"
```

```shell
pm2 start "docker run --gpus all -p 8007:80 faizanshk/atris-emotion"
```

```shell
pm2 start "docker run --gpus all -p 8006:8006 shazam22/atris-entity"
```

```shell
pm2 start "docker run --gpus all -p 8005:8005 beyonder99/atris_summerization"
```

```shell
pm2 start "docker run -p 1000:5000 quay.io/codait/max-ocr
```

> Celery Install

```shell
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install libmagic1
pip install python-magic
```
> Celery Running
```shell
pm2 start "celery -A task_worker_config worker -l INFO -Q stt_queue -c 20 -n worker1 -E"
```

```shell
pm2 start "celery -A task_worker_config worker -l INFO -Q entity_queue -c 4 -n worker2 -E"
```

```shell
pm2 start "celery -A task_worker_config worker -l INFO -Q summary_queue -c 4 -n worker3 -E"
```

> Flower Installation
```shell
virtualenv -p python3.8 flowerenv
source flowerenv/bin/activate
cd main-backend
pip install -r requirements.txt
pip install python-magic
pip install flower
```
> Flower Running
```shell
pm2 start "flower -A task_worker_config -port=5555 --basic_auth=admin:atris_admin"
```

> Save to Db Hook
```shell
pm2 start "gunicorn -w 9 -b 127.0.0.1:6000 -k uvicorn.workers.UvicornWorker main:app --timeout 120"
```
## Typesense
```shell
docker run -p 8108:8108 -v typesense-data:/data typesense/typesense:0.19.0 --data-dir /data --api-key=a882fbadb8add13fcfdf347c43c5f3e8acb71076fa76c59c04b03a7710939816895b8ac45bab80d1d3e67adc4e8d3a44ce38805e10aaada0e49b979a874c6801
```

## Main Endpoint
```shell
pm2 start "gunicorn -w 10 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app --timeout 120"
```
## Url Configs
DRON VM
```json
{
  "nemo": "http://52.152.166.196:7000/uploadfile/",
  "f_align": "http://52.152.166.196:8765/transcriptions?async=false",
  "sound_recog": "http://52.152.166.196:5000/model/predict?start_time=0",
  "smry_kwrds": "http://52.152.166.196:8005/get_summery/",
  "entty": "http://52.152.166.196:8006/detection/",
  "emot": "http://52.152.166.196:8007/analysis/",
  "ocr": "http://52.152.166.196:1000/model/predict",
  "image_label": "http://52.152.166.196:9000/model/predict"
}
```
DEVANSHI VM
```json
{
  "nemo": "http://13.68.236.211:7000/uploadfile/",
  "f_align": "http://13.68.236.211:8765/transcriptions?async=false",
  "sound_recog": "http://13.68.236.211:5000/model/predict?start_time=0",
  "smry_kwrds": "http://13.68.236.211:8005/get_summery/",
  "entty": "http://13.68.236.211:8006/detection/",
  "emot": "http://13.68.236.211:8007/analysis/",
  "ocr": "http://13.68.236.211:1000/model/predict",
  "image_label": "http://13.68.236.211:9000/model/predict"
}
```

## Redis KEY NAMES OF ENDPOINTS

1. Speech to text - `STT_UPLOAD_URL`
2. Forced Alignment - `FORCED_ALIGN_UPLOAD_URL`
3. Sound Recognition Endpoint - `SOUND_RECOG_ENDPOINT`
4. Summary Endpoint - `SUMMARY_KEYWORDS_ENDPOINT`
5. Entity Endpoint - `ENTITY_ENDPOINT`
6. Emotion Analysis Endpoint - `EMOTION_ANALYSIS_ENDPOINT`


