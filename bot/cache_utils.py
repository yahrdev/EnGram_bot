"""The functions for cache managing"""

from config import settings
import aioredis
from error_handlers import global_error_handler_sync, global_error_handler_async


@global_error_handler_sync
def initcache() -> aioredis.Redis:

    """init cache for the app"""

    redis = aioredis.from_url(
        f'redis://{settings.CACHE_REDIS_HOST}:{settings.CACHE_REDIS_PORT}/{settings.CACHE_REDIS_DB}'
    )

    return redis

    

class EngCache():

    """The class for cache processing"""

    def __init__(self, redis):
        self.redis = redis


    @global_error_handler_async
    async def set_key_with_ttl(self, key: str):

        """Init expiration time for our keys"""
        await self.redis.expire(key, settings.CACHE_DEFAULT_TIMEOUT)
        

    @global_error_handler_async
    async def add_update_to_cache(self, user_id, level = None):

        """Adding user data to cache. If level = None then level is not changed"""
        
        current_level = await self.redis.get(user_id)
        if current_level:
            current_level = current_level.decode('utf-8')
        if level == None:
            level = current_level
        if current_level != level:
            await self.redis.set(user_id, level)
        await self.set_key_with_ttl(user_id)  #update ttl everytime a user interacts with the bot
        return level
    


    @global_error_handler_async
    async def get_cached_user(self, user_id):

        """Retrieving data from cache"""

        level = await self.redis.get(user_id)
        if level:
            level = level.decode('utf-8')
            return level
        else:
            return None
        