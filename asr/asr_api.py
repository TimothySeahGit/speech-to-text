from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile

import logging
import sys
# sys.path.append('C:\\ffmpeg\\bin')
import os
import ffmpeg

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
# print(sys.path)
# logger.debug(sys.path)

app = FastAPI()

PORT: int  = 8001

# # Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="./wav2vec2")

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
    if len(file) > 10000000: # 10 Mb
        raise HTTPException(status_code=413, detail="File Size too big, limit is 10Mb")

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

    # resample to 16khz
    out, _ = (ffmpeg
        .input(temp_filepath)
        .output('-', format='mp3', acodec='libmp3lame', ar='16000')
        .overwrite_output()
        .run(capture_stdout=True)
    )
    
    os.remove(temp_filepath) 
    logger.debug(f"{temp_filepath} removed successfully") 

    # logger.debug(out)
    return {"transcription": pipe(out)['text'], "duration": "{:.2f}".format(float(duration))}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="debug", port=PORT)  