import redis
from django.conf import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST,
                                 port=settings.REDIS_PORT, db=0)


def check_request_limit(wallet_id):
    key = f'wallet:{wallet_id}:requests'
    current_requests = redis_client.get(key)

    if current_requests and int(current_requests) > 100:
        raise Exception('Превышен лимит запросов для этого кошелька')

    redis_client.incr(key)
    redis_client.expire(key, 60)
