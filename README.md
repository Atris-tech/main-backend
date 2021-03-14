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
  "nemo": "http://13.68.236.211:7000/uploadfile/",
  "f_align": "http://13.68.236.211:8765/transcriptions?async=false",
  "sound_recog": "http://13.68.236.211:5000/model/predict?start_time=0"
}
```

```
rq-dashboard -u redis://:D9iQsiD+4qUfmL9kQGIgvhLGB2tZnrv+tqoyo5prVfU=@paper.redis.cache.windows.net:6379/0

rq worker -c worker_config
```