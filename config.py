#the file for importing of the config settings


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    CACHE_REDIS_HOST: str
    CACHE_REDIS_PORT: int
    CACHE_REDIS_DB: int
    CACHE_TYPE: str
    CACHE_DEFAULT_TIMEOUT: int  #ttl for cache
    CACHE_KEY_PREFIX: str
    CACHE_CHECK_TIMEOUT: int  #how frequently check the ttl of the cache
    API_ASYNC_URL: str
    API_SYNC_URL: str
    ASYNC_API: bool
    

    model_config = SettingsConfigDict(env_file=".env", extra='allow')

settings = Settings()
