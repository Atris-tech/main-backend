from jose import JWTError, jwt
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import nlu
model = nlu.load('emotion')

class Text(BaseModel):
    text: str

app = FastAPI()

def verify_token(request):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization Error"
        )
    token = token.split()
    token = token[1]
    try:
        payload = jwt.decode(token, "09d25e094fdf6ca25d6c81f166b7a9563g93f7099h6f0f4caa6cfj3b88e8d3e7",
        algorithms=["HS256"])
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Authorization Error"
        )

@app.post("/analysis/")
async def emotion_analysis(text_obj: Text, request: Request):
    verify_token(request)
    try:
        emotion_frame = model.predict(text_obj.text, output_level="document", metadata=True)
        return emotion_frame.to_dict()["emotion"][0]
    except Exception as e:
        return {"emotion": None}
