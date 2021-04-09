from fastapi import Depends, WebSocket, \
    WebSocketDisconnect
import json
import aioredis
import asyncio
from settings import REDIS_URI, active_connections, get_ws_clients


async def redis_connector(client_id, websocket: WebSocket, clients=Depends(get_ws_clients)):
    async def consumer_handler(ws: WebSocket, r):
        try:
            while True:
                """runs when web socket receives text from web"""
                _ = await ws.receive_text()
                # if message:
                #     print(message)
                #     await r.publish("chat:c", message)
        except WebSocketDisconnect as exc:
            for dic in active_connections:
                dic["websocket"] = websocket
                active_connections.remove(dic)
                break
            print(active_connections)

    async def producer_handler(channel):
        try:
            while True:
                message = await channel.get()
                if message:
                    print("message")
                    try:
                        data = json.loads(message.decode("utf-8"))
                        client_id = data["client_id"]
                        for dic in clients:
                            if dic["id"] == client_id:
                                ws = dic["websocket"]
                                print(data)
                                print(data["data"])
                                await ws.send_text(json.dumps(data["data"]))
                    except Exception as e:
                        print(e)
        except Exception as exc:
            print(exc)

    redis = await aioredis.create_redis_pool(address=REDIS_URI, ssl=True)
    (channel,) = await redis.subscribe(str(client_id))
    consumer_task = consumer_handler(ws=websocket, r=redis)
    producer_task = producer_handler(channel)
    await asyncio.wait(
        [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    print("I am called redis close")
    redis.close()
    await redis.wait_closed()
