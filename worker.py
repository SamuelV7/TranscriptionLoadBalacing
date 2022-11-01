from dotenv import load_dotenv
import os
import redis
import json 

load_dotenv()
REDIS_URL = os.getenv('REDIS_URL')
r = redis.StrictRedis.from_url(REDIS_URL)


def get_job():
    if r.exists("sermon-scribe-queue") is False:
        return None
    data_string = r.rpop('sermon-scribe-queue')
    # if data_string ==
    data = json.loads(data_string)
    return data


def save(key: str, value: str):
    r.set(key, value)
