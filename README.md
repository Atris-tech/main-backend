"# main-backend" 
rq-dashboard -u redis://:D9iQsiD+4qUfmL9kQGIgvhLGB2tZnrv+tqoyo5prVfU=@paper.redis.cache.windows.net:6379/0

rq worker -c worker_config

```
docker commit `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` jainal09/nemo:latest
docker exec -it `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'` bash
docker stop `docker ps | grep 'jainal09/nemo:latest' |awk '{ print $1 }'`
```
