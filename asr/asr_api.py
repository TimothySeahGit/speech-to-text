from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, UploadFile

import logging
import sys

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

PORT: int  = 8001


@app.on_event("startup")
def startup_event():
    print("The port used for this app is", PORT)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/ping/")
def ping():
    return {"message": "pong"}

@app.post("/asr/")
async def create_file(file: Annotated[bytes, File()]):
    logger.debug(f'File size: {len(file)}')
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", log_level="debug", port=PORT)  