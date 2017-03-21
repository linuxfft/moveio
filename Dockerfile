# Version 0.1

# Set the base image to Ubuntu

FROM python:3.5-alpine

# File Author / Maintainer

MAINTAINER fengzhitao@empower.cn

ADD . /moveio/

RUN pip install -r /moveio/requirements.txt -i https://pypi.douban.com/simple

CMD python /moveio/download.py

WORKDIR /moveio/
