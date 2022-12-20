from dotenv import load_dotenv
import redis
import os
import pytest
import main

@pytest.fixture(scope="module")
def redis_db():
    load_dotenv()
    r = redis.StrictRedis.from_url(os.getenv('REDIS_URL'))
    yield r
    print("closing connection to redis")
    #r.close()

def test_get_job(redis_db):
    # add somthing to list and check it is there
    q_name, value = 'test_q',  "testing_q"
    redis_db.lpush(q_name, value)

    #confirm data is the entered data
    data = redis_db.rpop(q_name)
    assert str(data, encoding='utf-8') == value

def test_save_result_db(redis_db):
    key, value = 'test_db',  "testing_job"
    main.save_result_db(key, value)
    assert str(redis_db.get(key), encoding='utf-8') == value
    redis_db.delete(key)
