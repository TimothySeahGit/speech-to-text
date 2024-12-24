from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, UploadFile

import logging
import sys
import os


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

PORT: int  = 8001

# # Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="./models")

# import ffmpeg
# duration = ffmpeg.probe(local_file_path)["format"]["duration"]


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
    # TODO: enforce a file size limit
    # TODO: resample audio to 16000hz

    return {"file_size": len(file), "transcribed": pipe(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", log_level="debug", port=PORT)  