# speech-to-text

### Part 2: Running the automatic speech recognition api

Run the docker image:
```
docker build -t stt-asr:v1 .

docker run -p 8001:8001 stt-asr:v1
```
Run the script to process the data:
```
pip install pandas
python asr/cv-decode.py
```

  
### Part 7: Accessing the hosted search app
```
http://<redacted>.compute-1.amazonaws.com:3000/
```
You can search in the free text field on age, gender, accent, and generated_text. Autocomplete suggestions will be made based on generated_text.

You can further filter on duration of the mp3 file and age, gender, accent.

Some fun snippets to try are 'vanish', 'prognos', 'begin'...
