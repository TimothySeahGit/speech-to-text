import zipfile
import os
import shutil
import requests
import pandas as pd

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

def __call_api(file_name):
    """
    Call the API.

    Args:
        file_name (str): The filename of the mp3 to be transcribed.
    """

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


def get_transcription(source_path, filename):
    """
    Get the speech-to-text transcription for a file.

    Args:
        source_path (str): The location of the files.
        file_name (str): The filename of the mp3 to be transcribed.
    
    Returns:
        generated_text (str): The transcribed text.
        duration (str): The duration of the mp3 file, in seconds.
    """
    if os.path.exists(source_path + filename):
        print('processing ', filename)
        response_json = __call_api(source_path + filename).json()
        return response_json['transcription'].lower(), response_json['duration']
    else:
        err = 'ERROR! File not found in source directory'
        print(err)
        return err, 'err'


dataframe = pd.read_csv('cv-valid-dev.csv')

dataframe[['generated_text','duration']] = dataframe.apply(lambda x: get_transcription(source_path, x['filename'].split('/')[-1]), 
                                                            axis=1, result_type="expand")

# could consider saving batches in future
dataframe.to_csv('cv-valid-dev.csv', index=False)