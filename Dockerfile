# Version 0.1

# Set the base image to Ubuntu

FROM python:3.5-alpine

# File Author / Maintainer

MAINTAINER fengzhitao@empower.cn

ADD ./requirements.txt /
RUN pip install -r /requirements.txt -i https://pypi.douban.com/simple

ADD . /moveio/

WORKDIR /moveio/

ENTRYPOINT ["/bin/sh", "consumer.sh"]

COPY image_list.yml image_list.yml_bak


