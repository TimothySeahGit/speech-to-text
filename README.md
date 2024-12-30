# speech-to-text

### Part 2: Running the automatic speech recognition api

Run the docker image:
```
docker build -t stt-asr:v1 .

docker run -p 8001:8001 stt-asr:v1
```
Download common_voice.zip to the project root folder.
Run the script to process the data:
```
pip install pandas
python asr/cv-decode.py
```

  
### Part 7: Accessing the hosted search app
```
http://ec2-3-82-42-191.compute-1.amazonaws.com:3000/
```
You can search in the free text field on age, gender, accent, and generated_text. Autocomplete suggestions will be made based on generated_text.

You can further filter on duration of the mp3 file and age, gender, accent.

Some fun snippets to try are 'vanish', 'prognos', 'begin'...

#
#### (optional) helper commands for building the docker-compose.yaml on an ec2 instance
```
yum install git -y
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -a -G docker $USER

## git clone this repo and restart shell before proceeeding ##

chmod +x -R search-ui/
chmod +x -R elastic-backend/
sudo systemctl start docker
docker-compose up
```