import base64
import re

import yake
from fastapi import FastAPI, Request, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel
from summarizer import Summarizer

model = Summarizer(model="bert-large-uncased")

language = "en"
max_ngram_size = 1
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 20


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


@app.post("/get_summery/")
async def summarizer(text_obj: Text, request: Request):
    verify_token(request)
    data = dict()
    text = None
    try:
        b64_string_binary = text_obj.text.encode('utf-8')
        binary_text = base64.b64decode(b64_string_binary)
        to_summarize_string = binary_text.decode('utf8')
        to_summarize_string = to_summarize_string.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace(
            '\\n', ' ').replace('\\', ' ')
        to_summarize_string = re.sub(' +', ' ', to_summarize_string)
        to_summarize_string = to_summarize_string.replace('\\', ' ')
        result = model(to_summarize_string, min_length=60, num_sentences=3)
        text = ''.join(result)
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\\n', ' ').replace('\\', ' ')
        text = re.sub(' +', ' ', text)
        text = text.replace('\\', ' ')
        data["summary"] = text
        notes_keywords = list()
        custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                                    dedupFunc=deduplication_algo, windowsSize=windowSize,
                                                    top=numOfKeywords, features=None)
        keywords = custom_kw_extractor.extract_keywords(text)
        for kw in keywords:
            if kw not in notes_keywords:
                notes_keywords.append(kw)
        data["keywords"] = notes_keywords
        return data
    except Exception as e:
        print(e)
        if text is not None:
            return {"summary": text, "keyword": None}
        else:
            return {"summary": None, "keyword": None}
