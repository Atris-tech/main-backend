# main-backend

```
docker commit `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` jainal09/nemo:latest
docker exec -it `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` bash
docker stop `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'`
```

```
screen -S d_gentle
docker run --restart always -p 8765:8765 lowerquality/gentle
```

```
screen -S d_stt
docker run --restart always --gpus all -p 7000:7000 jainal09/nemo:latest
```

```
screen -S d_max-audio
docker run --restart always -p 5000:5000 -it quay.io/codait/max-audio-classifier
```

```
screen -S d_image_label
docker run --restart always -p 9000:5000 -it quay.io/codait/max-resnet-50
```

```
screen -S d_emotion
docker run --restart always --gpus all -p 8007:80 faizanshk/atris-emotion
```

```
screen -S d_entity
docker run --restart always --gpus all -p 8006:8006 shazam22/atris-entity
```

```
screen -S d_summary
docker run --restart always --gpus all -p 8005:8005 beyonder99/atris_summerization
```

```
screen -S d_ocr
docker run --restart always -it -p 1000:5000 quay.io/codait/max-ocr
```

```
screen -S celery-stt
celery -A task_worker_config worker -l INFO -Q stt_queue -c 20 -n worker1 -E
```

```
screen -S celery-entity
celery -A task_worker_config worker -l INFO -Q entity_queue -c 4 -n worker2 -E
```

```
screen -S celery-summary
celery -A task_worker_config worker -l INFO -Q summary_queue -c 4 -n worker3 -E
```

```
screen -S celery-flower
source env1/bin/activate
cd main-backend
flower -A task_worker_config -port=5555 --basic_auth=admin:atris_admin
```

`Ctrl+a` `d`

```
screen -ls
screen -r {{id}}
```

```
docker run -p 8108:8108 -v typesense-data:/data typesense/typesense:0.19.0 --data-dir /data --api-key=a882fbadb8add13fcfdf347c43c5f3e8acb71076fa76c59c04b03a7710939816895b8ac45bab80d1d3e67adc4e8d3a44ce38805e10aaada0e49b979a874c6801
```

```json
{
  "nemo": "http://20.39.54.134:7000/uploadfile/",
  "f_align": "http://20.39.54.134:8765/transcriptions?async=false",
  "sound_recog": "http://20.39.54.134:5000/model/predict?start_time=0",
  "smry_kwrds": "http://20.39.54.134:8005/get_summery/",
  "entty": "http://20.39.54.134:8006/detection/",
  "emot": "http://20.39.54.134:8007/analysis/"
}
```

## Redis KEY NAMES OF ENDPOINTS

1. Speech to text - `STT_UPLOAD_URL`
2. Forced Alignment - `FORCED_ALIGN_UPLOAD_URL`
3. Sound Recognition Endpoint - `SOUND_RECOG_ENDPOINT`
4. Summary Endpoint - `SUMMARY_KEYWORDS_ENDPOINT`
5. Entity Endpoint - `ENTITY_ENDPOINT`
6. Emotion Analysis Endpoint - `EMOTION_ANALYSIS_ENDPOINT`

```
rq-dashboard -u redis://:D9iQsiD+4qUfmL9kQGIgvhLGB2tZnrv+tqoyo5prVfU=@paper.redis.cache.windows.net:6379/0

rq worker -c worker_config
```

NLP Deployment authentication.

Entity

```
id: shazam22
password : Infamous123
```

Summarization

```
id: beyonder99
password : Infamous123
```

Emotion

```
id : faizanshk
Password : 4nSH4VHE;KvBap%
```