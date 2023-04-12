from dataclasses import dataclass
import os, ffmpeg, json, redis, whisper, pytube
from typing import Optional

# create redis stream if it doesn't exist, redis url
@dataclass
class SermonYT:
    name: str
    url: str

@dataclass
class Sermon:
    sermon : SermonYT
    transcript: str

class RedisDB:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(redis_url)
    
    def create_group(self, stream_name, group_name):
        self.redis.xgroup_create(stream_name, group_name, id=0, mkstream=True)

    # add message to stream
    def add_message_to_stream(self, stream_name:str, message: SermonYT):
        # convert to json
        url = message.url
        message = message.__dict__
        self.redis.xadd(stream_name, message)
    
    def add_transcript(self, sermon: Sermon):
        self.redis.set(sermon.url, sermon.__dict__)
        return
    
    # get messages from stream acknowledge them
    def get_messages(self, stream_name:str, group_name:str, consumer_name:str):
        # read pending messages
        # Get the list of individual pending messages using xclaim
        # get one message from stream
        messages = self.redis.xreadgroup(group_name, consumer_name, {stream_name: '>'}, count=1, block=0)
        if messages:
            stream, message = messages[0]
            # acknowledge message
            self.redis.xack(stream_name, group_name, message[0][0])
        else:
            print("No messages")
        
        converted = messages[0][1][0][1]
        converted = {key.decode('utf-8'): value.decode('utf-8') for key, value in converted.items()}
        return converted

    def get_all_sermons(self) -> list:
        sermons = self.redis.keys()
        return sermons
    
class Transcribe:
    def __init__(self, model:str):
        self.model = whisper.load_model(model)
        return 
    
    def transcribe(self, audio_file_path: str, language: str) -> str:
        result = self.model.transcribe(audio_file_path, language=language)
        self.result = {'name': audio_file_path, 'result': result, 'text': result['text']}
        return self.result
    
    # batch transcribe
    def batch_transcribe(self, audio_location: list):
        self.transcripts = [{'name': audio, 'text': self.transcribe(audio)['text']} for audio in audio_location]
        return self.transcripts
    
    def save_transcripts(self, transcripts: list):
        for transcript in transcripts:
            with open(transcript['name'] + '.txt', 'w') as f:
                f.write(transcript['text'])
        return
    
    def save_transcript(self, file_name, text):
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(text)
        
class Worker:
    def __init__(self, redis_url, model):
        self.redis = RedisDB(redis_url)
        self.model = Transcribe(model)
        return

    # get message and transcribe and add to database
    def work(self):
        # get one message from stream
        self.current = self.redis.get_messages()
        print(self.current)
    
    def save_transcript_db(self, file_name, url, text):
        sermon = SermonYT(file_name, url, text)
        self.redis.add_transcript(sermon=sermon)
        return


class YouTube:
    def __init__(self, url):
        self.yt = pytube.YouTube(url)
        self.url = url
        self.title = self.yt.title
        return
    
    def download_mp3(self, output_file_name: Optional[str] = None) -> str:
        yt = pytube.YouTube(self.url)
        # check if mp3 version exist
        if os.path.exists(new_file):
            return new_file
        
        if output_file_name is None:
            new_file = f"{yt.title}.mp3"
        else:
            new_file = f"{output_file_name}.mp3"
        
        # new_file = yt.title.replace('"', '')
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if yt.title == "Video Not Available":
            raise Exception("Video Not Available")
        
        print("Downloading...")
        output_dir = 'mp3'
        file_name = audio_stream.download(output_path = output_dir)
        
        # Audio conversion
        print("Converting to mp3")
        stream = ffmpeg.input(file_name)
        stream = ffmpeg.output(stream, new_file)
        ffmpeg.run(stream)
        return new_file