import yaml
import os
import shutil

from redis.connection import ConnectionPool
from huey import RedisHuey


# copy setting file
images_file_name = 'image_list.yml'
if not os.path.getsize(images_file_name):
    shutil.copy(images_file_name + "_bak", images_file_name)

setting_file_name = 'settings.yml'
if not os.path.getsize(setting_file_name):
    shutil.copy(setting_file_name + "_bak", setting_file_name)

with open('settings.yml', 'rt') as f:
    settings = yaml.load(f)


redis_pool = ConnectionPool.from_url(settings['REDIS_URL'])
docker_huey = RedisHuey('docker_huey', connection_pool=redis_pool)





