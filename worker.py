
from dotenv import load_dotenv
import os
import redis
import json 

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL')

r = redis.StrictRedis.from_url(REDIS_URL)


def getJob():
    data_string = r.rpop('sermon-scribe-queue')
    data = json.loads(data)
    return data


