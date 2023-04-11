import redis
import whisper

# create redis stream if it doesn't exist, redis url
class Redis:
    def __init__(self, stream_name, redis_url):
        self.stream_name = stream_name
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(redis_url)
        self.redis.xgroup_create(self.stream_name, 'group', mkstream=True)
    
    # add message to stream
    def add_message(self, message):
        self.redis.xadd(self.stream_name, message)
    
    # get messages from stream acknowledge them
    def get_messages(self):
        # get one message from stream
        messages = self.redis.xreadgroup('group', 'consumer', {self.stream_name: '>'}, count=1, block=0)
        if messages:
            stream, message = messages[0]
            print(message)

            # acknowledge message
            self.redis.xack(self.stream_name, 'group', message[0])
        else:
            print("No messages")
        return messages
    
class Transcribe:
    def __init__(self, model:str):
        self.model = whisper.load_model(model)
        return 
    
    def transcribe(self, audio_file_path: str) -> str:
        self.result = self.model.transcribe(audio_file_path, language='en')
        return self.result
    
    def text(self):
        return self.result['text']


    

