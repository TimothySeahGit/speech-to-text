from typing import Annotated

import uvicorn
from fastapi import FastAPI, File, UploadFile

import logging
import sys
import os
import ffmpeg

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

PORT: int  = 8001

# # Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="./models")

# import ffmpeg
# duration = ffmpeg.probe(local_file_path)["format"]["duration"]
temp_filepath = 'input.mp3'


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
def create_file(file: Annotated[bytes, File()]):
    logger.debug(f'File size: {len(file)}')
    # TODO: enforce a file size limit
    # TODO: resample audio to 16000hz
 
    process = (
        ffmpeg
        .input('pipe:0')
        .output(temp_filepath, format='mp3')
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
    process.stdin.write(file)
    process.stdin.close()
    process.wait()

    duration = ffmpeg.probe(temp_filepath)["format"]["duration"]

    return {"transcription": pipe(file), "duration": "{:.2f}".format(float(duration))}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", log_level="debug", port=PORT)  