import mongoengine
import uvicorn
from fastapi import FastAPI, Depends, WebSocket, status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import settings
from api.api import api_router
from api.websocket_redis_connector import redis_connector
from db_models.models.user_model import UserModel
from settings import get_ws_clients

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=None,
    redoc_url=None
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET_KEY)

app.include_router(api_router, prefix="/api")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id: str, websocket: WebSocket, clients=Depends(get_ws_clients)):
    await websocket.accept()
    try:
        UserModel.objects.get(id=str(client_id))
        connected_client = {
            "id": client_id,
            "websocket": websocket
        }
        clients.append(connected_client)
        await redis_connector(client_id, websocket, clients)

    except(UserModel.DoesNotExist, mongoengine.ValidationError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
