# -*- encoding: utf8 -*-
import docker
import threading
import yaml


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
            print('='*50)
            # 下载镜像
            image = client.images.pull(self.image, tag=self.tag)
            # 打标签
            new_tag = self.image + '_' + self.tag
            image.tag(self.repository, new_tag)
            # push
            print(self.repository)
            ret = client.images.push(self.repository, tag=new_tag, auth_config={'username': self.username,
                                                                                 'password': self.password})
            print(ret)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    with open('usage.yml', 'rt') as f:
        setting = yaml.load(f)

    threads = [MoveIO(host=setting['host'], repository=setting['repository'], username=setting['username'], password=setting['password'],
                      image=item['name'], tag=item['tag']) for item in setting['images']]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
