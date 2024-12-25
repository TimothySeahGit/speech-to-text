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
    """
    if os.path.exists(source_path + filename):
        response = __call_api(source_path + filename)
        print(filename)
        return response.json()['transcription'].lower()
    else:
        err = 'ERROR! File not found in source directory'
        print(err)
        return err




all_files = os.listdir(source_path)
print(all_files[:5])

dataframe = pd.read_csv('cv-valid-dev.csv')

# for filename in dataframe['filename']:
#     mp3_filename = filename.split('/')[-1]

#     transcription = __get_transcription(source_path + mp3_filename)
#     print(transcription.json()['transcription'])



dataframe['generated_text'] = dataframe['filename'].map(lambda x: get_transcription(source_path, x.split('/')[-1]))

dataframe.to_csv('cv-valid-dev.csv', index=False)