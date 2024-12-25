from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile

import logging
import sys
sys.path.append('/c/ffmpeg/bin')
import os
import ffmpeg

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

PORT: int  = 8001

# # Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="./models")

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


    # TODO: resample audio to 16000hz
    # process = (
    #     ffmpeg
    #     .input('pipe:0')
    #     .output('pipe:', format='mp3', acodec='libmp3lame', ar='16000')
    #     .run_async(pipe_stdin=True, pipe_stderr=True)
    # )
#     process = (
#     ffmpeg
#     .input(in_filename)
#     .output('pipe':, format='rawvideo', pix_fmt='rgb24')
#     .run_async(pipe_stdout=True, pipe_stderr=True)
# )

    out, _ = (ffmpeg
        .input(temp_filepath)
        .output('-', format='mp3', acodec='libmp3lame', ar='16000')
        .overwrite_output()
        .run(capture_stdout=True)
    )
    
    os.remove(temp_filepath) 
    logger.debug(f"{temp_filepath} removed successfully") 

    # output_file = 'output.mp3'
    # cmd_str = f"ffmpeg -i {temp_filepath} -c:a libmp3lame -ar 16000 {output_file} -y"
    # os.system(cmd_str)
    # logger.debug(out)
    return {"transcription": pipe(out), "duration": "{:.2f}".format(float(duration))}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", log_level="debug", port=PORT)  