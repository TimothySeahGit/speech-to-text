import zipfile
import os
import shutil
import requests

archive = zipfile.ZipFile('common_voice.zip')

source_path = 'cv-valid-dev/cv-valid-dev/'
if os.path.exists(source_path) and os.path.isdir(source_path):
    shutil.rmtree(source_path)


# extract from zip file
for file in archive.namelist():
    if file.startswith(source_path) and file.endswith('.mp3'):
        archive.extract(file, '.')
    if file == 'cv-valid-dev.csv':
        archive.extract(file, '.')

def __get_transcription(file_name):

    headers = {
        'accept': 'application/json',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    files = {
        'file': (file_name, open(file_name, 'rb'), 'audio/mpeg'),
    }

    response = requests.post('http://127.0.0.1:8001/asr/', headers=headers, files=files)

    return response


all_files = os.listdir(source_path)
print(all_files[:5])

for mp3_filename in all_files[:5]:

    transcription = __get_transcription(source_path + mp3_filename)
    print(transcription.json()['transcription'])
