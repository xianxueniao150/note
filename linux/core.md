## 配置ubuntu20内核转储功能
```sh
# 查看当前转储文件大小
ulimit -c
为0，表示当前转储文件大小为0，没有启动内核转储

#设置coredump 大小为无限大
ulimit -c unlimited 
```
