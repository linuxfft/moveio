# -*- encoding: utf8 -*-
import os
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images', nargs='*', type=str, required=True)
    parser.add_argument('--host', type=str, default='registry.cloudahead.info')
    parser.add_argument('-p', '--project', type=str, required=True)

    return parser.parse_args()


def push_docker_images():
    args = get_args()

    images = args.images
    host = args.host
    project = args.project
    tag_prefix = host + ':' + project

    for item in images:
        try:
            # 下载镜像
            print('image: ', item)
            os.system('docker pull ' + item)

            # 登陆服务器
            print('host: ', host)
            os.system('docker login ' + host)

            # 打标签
            tag = tag_prefix + '/' + item
            print('tag: ', item,  tag)
            os.system('docker tag ' + item + ' ' + tag)

            # push
            os.system('docker push ' + tag)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    push_docker_images()
