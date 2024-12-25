FROM python:3.9.18
RUN apt-get -y update
RUN apt-get install -y ffmpeg
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# download the model from huggingface
COPY download_model.py ./
RUN python download_model.py

# Copy in the source code
COPY asr ./asr
EXPOSE 8001

CMD ["uvicorn", "asr.asr_api:app", "--host", "0.0.0.0", "--port", "8001"]