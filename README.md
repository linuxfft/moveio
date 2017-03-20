## 功能
先在aliyun北美结点pull需要的image，然后再push回（本地）指定的仓库（registry）

## 用法
```
sudo python download.py
```

## 使用docker
```
    sudo docker build -t moveio .
    sudo docker-compose -f ./docker-compose.yml up
```