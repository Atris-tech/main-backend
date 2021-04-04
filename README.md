# main-backend

```
docker commit `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` jainal09/nemo:latest
docker exec -it `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` bash
docker stop `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'`
```

```
docker run -p 8765:8765 lowerquality/gentle
docker run -p 5000:5000 -it quay.io/codait/max-audio-classifier
docker run --gpus all -p 7000:7000 jainal09/nemo:latest
celery -A task_worker_config worker -l INFO -Q stt_queue -c 20 -n worker1 -E
```
```
docker run -p 8108:8108 -v typesense-data:/data typesense/typesense:0.19.0 --data-dir /data --api-key=a882fbadb8add13fcfdf347c43c5f3e8acb71076fa76c59c04b03a7710939816895b8ac45bab80d1d3e67adc4e8d3a44ce38805e10aaada0e49b979a874c6801
```

```
screen -S gentle
screen -S celery-stt
screen -S stt
screen -S max-audio
```
`Ctrl+a` `d`

```
screen -ls
screen -r {{id}}
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