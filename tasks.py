import docker
from app import docker_huey
from app import settings
import logging.config

logging.config.fileConfig('logger.ini')

RUN = 'running'
LOG = logging.getLogger('logger01')
client = docker.from_env(version='1.24')


@docker_huey.task(retries=3, retry_delay=180)
def sync_image(blue_print):
    blue_print.start()


class BluePrint(object):
    state = None
    started = 0

    def __init__(self, src_image):
        self.src_image = src_image

    def start(self):
        image_obj = client.images.pull(self.src_image['name']+':'+self.src_image['tag'])

        # tag image
        new_tag = '{}_{}'.format(self.src_image['name'].replace('/', '_'), self.src_image['tag'])
        LOG.info('tag image: ' + new_tag)
        image_obj.tag(settings['REPOSITORY'], new_tag)

        # push
        LOG.info('push image: ' + new_tag + ' ' + settings['REPOSITORY'])
        client.images.push(settings['REPOSITORY'], tag=new_tag, auth_config={'username': settings['USERNAME'],
                                                                      'password': settings['PASSWORD']})
        LOG.info('push successed: ' + new_tag)


def create_sync_blue_print(src_image):
    return BluePrint(src_image)
