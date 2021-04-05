from jose import JWTError, jwt
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import spacy
import base64
import re

print(spacy.prefer_gpu())
nlp = spacy.load("en_core_web_lg")


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
        jwt.decode(token, "09d25e094fdf6ca25d6c81f166b7a9563g93f7099h6f0f4caa6cfj3b88e8d3e7",
                   algorithms=["HS256"])
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Authorization Error"
        )


@app.post("/detection/")
async def entity_detection(text_obj: Text, request: Request):
    verify_token(request)
    try:
        b64_string_binary = text_obj.text.encode('utf-8')
        binary_text = base64.b64decode(b64_string_binary)
        to_process_text = binary_text.decode('utf8')
        to_process_text = to_process_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\\n', ' ').replace('\\', ' ')
        to_process_text = re.sub(' +', ' ', to_process_text)
        to_process_text = to_process_text.replace('\\', ' ')
        doc = nlp(to_process_text)
        labels = []
        for entity in doc.ents:
            if entity.label_ in labels:
                pass
            else:
                labels.append(entity.label_)
        my_dict = dict()

        for key in labels:
            my_dict[key] = []
        for entity in doc.ents:
            if entity.text not in my_dict[entity.label_]:
                my_dict[entity.label_].append(entity.text)
        return my_dict
    except Exception as e:
        print(e)
        return {"Entity": None}
