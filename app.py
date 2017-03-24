import logging.config
import yaml
import os
import shutil

from redis.connection import ConnectionPool
from huey import RedisHuey


logging.config.fileConfig('logger.ini')
logger = logging.getLogger()

# copy setting file
setting_file_name = 'usage.yml'
if not os.path.getsize(setting_file_name):
    shutil.copy(setting_file_name + "_bak", setting_file_name)

with open('settings.yml', 'rt') as f:
    settings = yaml.load(f)


redis_pool = ConnectionPool.from_url(settings['REDIS_URL'])
docker_huey = RedisHuey('docker_huey', connection_pool=redis_pool)





