# -*- encoding: utf8 -*-
import logging
import logging.config
import threading
import docker
import yaml
from docker.errors import ImageNotFound
import time
import datetime
import os
import sched

logging.config.fileConfig('logger.ini')
schedule = sched.scheduler(time.time, time.sleep)

threadList = []


class MoveIO(threading.Thread):
    """Download image and push to remote repository"""
    def __init__(self,  host, username, repository, password, image, tag='latest'):
        threading.Thread.__init__(self)
        self.host = host
        self.username = username
        self.password = password
        self.image = image
        self.tag = tag
        self.repository = host+'/' + repository

    def run(self):
        try:
            client = docker.from_env()
            # pull image
            logging.info('pull image: ' + self.image + ':' + self.tag)
            try:
                # if get method not found image, then throw ImageNotFound exception
                locate_image = client.images.get(self.image + ':' + self.tag)
                image = client.images.pull(self.image, tag=self.tag)
                if image.id == locate_image.id:
                    logging.info(self.image + ':' + self.tag + ' is the latest' + '***')
                    return
            except ImageNotFound:
                image = client.images.pull(self.image, tag=self.tag)

            # tag image
            new_tag = self.image + '_' + self.tag
            logging.info('tag image: ' + new_tag)
            image.tag(self.repository, new_tag)

            # push
            logging.info('push image: ' + new_tag + ' ' + self.repository)
            client.images.push(self.repository, tag=new_tag, auth_config={'username': self.username,
                                                                                'password': self.password})
            logging.info('push successed: ' + new_tag)
        except Exception as e:
            logging.error(e)


def push_image():
    sleep_time = 60

    try:
        with open('usage.yml', 'rt') as f:
            setting = yaml.load(f)

        threads = [MoveIO(host=setting['host'], repository=setting['repository'], username=setting['username'], password=setting['password'],
                          image=item['name'], tag=item['tag']) for item in setting['images']]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        logging.info('log clean method going to sleep ' + str(sleep_time / 60) + ' minute')
        schedule.enter(sleep_time, 0, push_image)

    except Exception as e:
        logging.error(e)


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
    schedule.enter(1, 0, push_image)
    schedule.enter(2, 0, clean_log)
    schedule.run()
