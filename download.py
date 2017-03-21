# -*- encoding: utf8 -*-
import logging
import logging.config
import docker
import yaml
from docker.errors import ImageNotFound
import time
import datetime
import os
import sched
import shutil
from multiprocessing.dummy import Pool as ThreadPool

# copy configure file
file_name = 'usage.yml'
if not os.path.getsize(file_name):
    shutil.copy(file_name + "_bak", file_name)

logging.config.fileConfig('logger.ini')
schedule = sched.scheduler(time.time, time.sleep)

host = ''
username = ''
repository = ''
password = ''


def push_image(image):
    # print(image)
    image_name = image['name']
    tag = image['tag']
    try:
        client = docker.from_env()
        # pull image
        logging.info('pull image: ' + image_name + ':' + tag)
        try:
            # if get method not found image, then throw ImageNotFound exception
            locate_image = client.images.get(image_name + ':' + tag)
            image_obj = client.images.pull(image_name, tag=tag)
            if image_obj.id == locate_image.id:
                logging.info(image_name + ':' + tag + ' is the latest' + '***')
                return
        except ImageNotFound:
            image_obj = client.images.pull(image_name, tag=tag)

        # tag image
        new_tag = image_name + '_' + tag
        logging.info('tag image: ' + new_tag)
        image_obj.tag(repository, new_tag)

        # push
        logging.info('push image: ' + new_tag + ' ' + repository)
        client.images.push(repository, tag=new_tag, auth_config={'username': username,
                                                                      'password': password})
        logging.info('push successed: ' + new_tag)
    except Exception as e:
        logging.error(e)


def run_push_image():
    global host
    global username
    global password
    global repository

    sleep_time = 60

    try:
        with open('usage.yml', 'rt') as f:
            setting = yaml.load(f)

        host = setting['host']
        repository = setting['repository']
        username = setting['username']
        password = setting['password']
        repository = host + '/' + repository

        # print(setting['images'])
        pool = ThreadPool(100)
        pool.map(push_image, setting['images'])
        pool.close()
        pool.join()

        logging.info('push image method going to sleep ' + str(sleep_time / 60) + ' minute')
        schedule.enter(sleep_time, 0, run_push_image)
    except Exception as e:
        logging.log(e)


def clean_log():
    clean_time = '03:00:00'
    interval_day = 1
    log_keep_time = 1
    log_dir = 'log'

    # calculate sleep time
    now_datetime = datetime.datetime.now()
    future_datetime = now_datetime + datetime.timedelta(days=interval_day)
    future_date = future_datetime.strftime('%Y-%m-%d')
    new_datetime_str = future_date + ' ' + clean_time
    new_datetime = datetime.datetime.strptime(new_datetime_str, '%Y-%m-%d %H:%M:%S')
    diff_second = (new_datetime - now_datetime).seconds
    try:
        file_list = os.listdir(log_dir)
        for f in file_list:
            mtime = os.path.getmtime(os.path.join(log_dir, f))
            mdata = datetime.datetime.fromtimestamp(mtime)

            diff = now_datetime - mdata
            if diff.days > log_keep_time:
                os.remove(os.path.join(log_dir, f))

        # sleep and then repeat do clean action
        logging.info('log clean method going to sleep ' + str(diff_second/60) + ' minute')
        schedule.enter(diff_second, 0, clean_log)
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    pass
    # schedule.enter(1, 0, run_push_image)
    # schedule.enter(2, 0, clean_log)
    # schedule.run()
