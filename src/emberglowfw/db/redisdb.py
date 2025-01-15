import redis


def open_redis_con():
    return redis.StrictRedis(host='10.23.3.225', port=6379, db=0, password="o0WsuLfpl0", username="default")