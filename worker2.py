from core import RedisDB, Transcribe, Worker, YouTube, Sermon, SermonYT
from dotenv import load_dotenv
import os
# download youtube video
url = "https://www.youtube.com/watch?v=NOqEuSGSXKg"


downloader = YouTube(url)

title = downloader.title

# add to db
load_dotenv()
REDIS_URL = os.getenv('REDIS_URL')
redis = RedisDB(REDIS_URL)
sermon = SermonYT(title, url)
# make sure to check it does not already exist in the db before adding to stream

# create group
stream_name = 'sermons'
group_name = 's1'
# redis.create_group(stream_name, group_name)
redis.add_message_to_stream(stream_name, sermon)
#create consumer
consumer_name = 'c1'
out = redis.get_messages(stream_name, group_name, consumer_name)
print(type(out))
print(out['name'])