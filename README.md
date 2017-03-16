## 功能
先在aliyun北美结点pull需要的image，然后再push回（本地）指定的仓库（registry）

## 用法
```
sudo python download.py --images redis mongo --host 127.0.0.1 -p 5000
```