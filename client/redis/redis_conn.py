"""
Module for Redis data and interface
"""
# pylint: disable=too-few-public-methods,no-member
import os
import redis
import yaml

# Fallback for config file if needed (Kubernetes can override with env vars)
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')

def get_caching_data():
    """Function to get cache config for redis cache"""
    host = os.getenv('REDIS_HOST', 'localhost')  # Default Redis host
    port = os.getenv('REDIS_PORT', 6379)         # Default Redis port
    password = os.getenv('REDIS_PASSWORD', '')   # Default password is empty string

    config_dict = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_HOST": host,
        "CACHE_REDIS_PORT": int(port),
        "CACHE_REDIS_URL": f"redis://{host}:{port}/0"
    }
    return config_dict


class CoreRedisClient:
    """Class for defining the structure of Redis database"""
    def __init__(self):
        # Get environment variables or fallback to the config.yaml
        host = os.getenv('REDIS_HOST', 'localhost')  
        port = os.getenv('REDIS_PORT', 6379)         
        password = os.getenv('REDIS_PASSWORD', '')   

        self.client = redis.Redis(
            host=host,
            port=int(port),
            password=password,
            decode_responses=True
        )

    def redis_status(self):
        """Function for getting the health of redis"""
        try:
            self.client.ping()
            return "up"
        except redis.ConnectionError:
            return "down"
