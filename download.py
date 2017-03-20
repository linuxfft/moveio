# -*- encoding: utf8 -*-
import logging
import logging.config
import threading
import docker
import yaml
from docker.errors import ImageNotFound

logging.config.fileConfig('logger.ini')


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

if __name__ == '__main__':
    with open('usage.yml', 'rt') as f:
        setting = yaml.load(f)

    threads = [MoveIO(host=setting['host'], repository=setting['repository'], username=setting['username'], password=setting['password'],
                      image=item['name'], tag=item['tag']) for item in setting['images']]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
